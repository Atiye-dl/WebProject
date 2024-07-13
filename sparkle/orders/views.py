from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Order, OrderItem
from cart.utils.cart import Cart

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_invoice_email(order):
    # Prepare context for the email
    context = {'order': order, 'shipping_price': order.shipping_price}
    subject = f'Receipt for Order {order.id}'
    html_message = render_to_string('email_invoice.html', context)
    plain_message = strip_tags(html_message)  # Remove HTML tags for plain text version
    from_email = 'your-email@example.com'  # Sender's email
    to = order.user.email  # Recipient's email

    # Send the email with subject, plain text, and HTML message
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

@login_required
def create_order(request):
    cart = Cart(request)  # Retrieve the user's shopping cart
    total_price_of_items = cart.get_total_price()  # Calculate total price of items

    # Determine shipping price based on total price of items
    if total_price_of_items >= 100:
        shipping_price = 0  # Free shipping for orders over $100
    else:
        shipping_price = 15  # Standard shipping fee

    # Create a new order associated with the current user
    order = Order.objects.create(user=request.user, shipping_price=shipping_price)

    # Create OrderItem instances for each item in the cart
    for item in cart:
        OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity']
        )

    send_invoice_email(order)  # Send the invoice email after order creation
    cart.clear()  # Clear the cart after order creation
    return redirect('orders:pay_order', order_id=order.id)  # Redirect to payment page

@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Get the order or raise 404 if not found
    context = {'title': 'Checkout', 'order': order}  # Prepare context for checkout page
    return render(request, 'checkout.html', context)  # Render the checkout template

@login_required
def fake_payment(request, order_id):
    cart = Cart(request)  # Retrieve the user's shopping cart
    cart.clear()  # Clear the cart as part of the fake payment process
    order = get_object_or_404(Order, id=order_id)  # Get the order or raise 404 if not found
    order.status = True  # Mark the order as paid
    order.save()  # Save the order status
    return redirect('orders:user_orders')  # Redirect to user's orders page

@login_required
def user_orders(request):
    orders = request.user.orders.all()  # Retrieve all orders for the current user
    context = {'title': 'Orders', 'orders': orders}  # Prepare context for user orders page
    return render(request, 'user_orders.html', context)  # Render the user orders template
