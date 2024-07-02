from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from shop.models import Product
from .forms import AddProductForm

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
    products = Product.objects.all()
    context = {'title':'Products' ,'products':products}
    return render(request, 'products.html', context)


@user_passes_test(is_manager)
@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added Successfuly!')
            return redirect('dashboard:add_product')
    else:
        form = AddProductForm()
    context = {'title':'Add Product', 'form':form}
    return render(request, 'add_product.html', context)
