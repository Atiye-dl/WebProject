from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Order, OrderItem
from cart.utils.cart import Cart

#------------------------

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_invoice_email(order):
    context = {'order': order, 'shipping_price': order.shipping_price,}
    subject = f'Invoice for Order {order.id}'
    html_message = render_to_string('email_invoice.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'your-email@example.com'
    to = order.user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
#----------------------------------------------------
@login_required
def create_order(request):
    cart = Cart(request)
    total_price_of_items = cart.get_total_price()

    # Determine shipping price based on total price of items
    if total_price_of_items >= 100:
        shipping_price = 0
    else:
        shipping_price = 15
    order = Order.objects.create(user=request.user, shipping_price=shipping_price)
    
    for item in cart:
        OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity']
        )
    
    send_invoice_email(order)
    
    cart.clear()
    
    return redirect('orders:pay_order', order_id=order.id)

@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'title':'Checkout' ,'order':order}
    return render(request, 'checkout.html', context)


@login_required
def fake_payment(request, order_id):
    cart = Cart(request)
    cart.clear()
    order = get_object_or_404(Order, id=order_id)
    order.status = True
    order.save()
    return redirect('orders:user_orders')


@login_required
def user_orders(request):
    orders = request.user.orders.all()
    context = {'title':'Orders', 'orders': orders}
    return render(request, 'user_orders.html', context)