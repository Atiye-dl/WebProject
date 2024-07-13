from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Product

@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart, ensuring the user is not adding their own product."""
    cart = Cart(request)  # Initialize the cart using the current request
    product = get_object_or_404(Product, id=product_id)  # Fetch the product or return a 404 if not found
    
    # Check if the current user is the creator of the product
    if product.added_by == request.user:
        messages.error(request, "You cannot add your own product to the cart.")
        return redirect('shop:product_detail', slug=product.slug)

    form = QuantityForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'])
        messages.success(request, 'Added to your cart successfully.')
    return redirect('shop:product_detail', slug=product.slug)

@login_required
def show_cart(request):
    """Display the current user's cart."""
    cart = Cart(request)  # Initialize the cart using the current request
    context = {'title': 'Cart', 'cart': cart}  # Prepare context data for rendering
    return render(request, 'cart.html', context)  # Render the cart template with context data

@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    cart = Cart(request)  # Initialize the cart using the current request
    product = get_object_or_404(Product, id=product_id)  # Fetch the product or return a 404 if not found
    cart.remove(product)  # Remove the product from the cart
    return redirect('cart:show_cart')  # Redirect to the cart view
