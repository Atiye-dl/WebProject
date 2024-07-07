from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from shop.models import Product
from accounts.models import User
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, EditProductForm


def is_manager(user):
    try:
        if not user.is_manager:
            raise Http404
        return True
    except:
        raise Http404


@user_passes_test(is_manager)
@login_required
def products(request):
    products = Product.objects.filter(added_by=request.user)  # Filter products by manager
    context = {'title': 'Products', 'products': products}
    return render(request, 'products.html', context)


@user_passes_test(is_manager)
@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user  
            product.is_approved = False
            product.save()
            messages.success(request, 'Product added successfully! Awaiting admin approval.')
            return redirect('dashboard:add_product')
    else:
        form = AddProductForm()
    context = {'title': 'Add Product', 'form': form}
    return render(request, 'add_product.html', context)


@user_passes_test(is_manager)
@login_required
def delete_product(request, id):
    product = Product.objects.filter(id=id).delete()
    messages.success(request, 'Product has been deleted!', 'success')
    return redirect('dashboard:products')


@user_passes_test(is_manager)
@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated', 'success')
            return redirect('dashboard:products')
    else:
        form = EditProductForm(instance=product)
    context = {'title': 'Edit Product', 'form':form}
    return render(request, 'edit_product.html', context)


@user_passes_test(is_manager)
@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added Successfuly!')
            return redirect('dashboard:add_category')
    else:
        form = AddCategoryForm()
    context = {'title':'Add Category', 'form':form}
    return render(request, 'add_category.html', context)


@user_passes_test(is_manager)
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)  # Filter orders by the current manager
    context = {'title':'Orders', 'orders':orders}
    return render(request, 'orders.html', context)


@user_passes_test(is_manager)
@login_required
def order_detail(request, id):
    order = Order.objects.filter(id=id, user=request.user).first()  # Ensure order belongs to the current manager
    if not order:
        raise Http404("Order does not exist or you do not have permission to view it.")
    items = OrderItem.objects.filter(order=order).all()
    context = {'title':'order detail', 'items':items, 'order':order}
    return render(request, 'order_detail.html', context)


@login_required
@user_passes_test(is_manager)
def manager_sales(request):
    orders = Order.objects.filter(items__product__added_by=request.user).order_by('-created').distinct()
    context = {'title': 'Manager Sales', 'orders': orders}
    return render(request, 'manager_sales.html', context)
