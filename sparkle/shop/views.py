from datetime import timezone
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from shop.models import Product, Category,Comment
from cart.forms import QuantityForm
from .forms import CommentForm
from django.contrib.admin.views.decorators import staff_member_required

def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj


def home_page(request):
	products = Product.objects.filter(is_approved=True)
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


@login_required
def product_detail(request, slug):
    form = QuantityForm()
    product = get_object_or_404(Product, slug=slug ,is_approved=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
    comments = product.comments.filter(approved=True)  # Only show approved comments

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.has_purchased(product):
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user 
                new_comment.product = product
                new_comment.created_at = timezone.now()
                new_comment.save()
                messages.success(request, "Your comment has been submitted and is awaiting approval.")
                return redirect('shop:product_detail', slug=slug)
            else:
                messages.error(request, "You must purchase this product to leave a comment.")
        else:
            messages.error(request, "Invalid form submission. Please try again.")
    else:
        comment_form = CommentForm()

    context = {
        'title': product.title,
        'product': product,
        'form': form,
        'favorites': 'favorites' if not request.user.likes.filter(id=product.id).exists() else 'remove',
        'related_products': related_products,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'product_detail.html', context)

@staff_member_required
def approve_comments(request):
    if request.method == 'POST':
        comment_ids = request.POST.getlist('comment_ids')
        comments = Comment.objects.filter(id__in=comment_ids)
        comments.update(approved=True)
        messages.success(request, f'Approved {comments.count()} comments.')
    return redirect('admin:shop_comment_changelist')


@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)


def search(request):
	query = request.GET.get('q')
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


def filter_by_category(request, slug):
	"""when user clicks on parent category
	we want to show all products in its sub-categories too
	"""
	result = []
	category = Category.objects.filter(slug=slug).first()
	[result.append(product) \
		for product in Product.objects.filter(category=category.id).all()]
	# check if category is parent then get all sub-categories
	if not category.is_sub:
		sub_categories = category.sub_categories.all()
		# get all sub-categories products 
		for category in sub_categories:
			[result.append(product) \
				for product in Product.objects.filter(category=category).all()]
	context = {'products': paginat(request ,result)}
	return render(request, 'home_page.html', context)

