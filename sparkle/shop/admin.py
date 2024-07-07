from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import Category, Product, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'content', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f'Approved {queryset.count()} comments.')
        # Redirect to the custom view for approving comments
        url = reverse('shop:approve_comments')
        return redirect(url)

    approve_comments.short_description = 'Approve selected comments'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_approved')
    list_filter = ('is_approved', 'category')
    actions = ['approve_products']

    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'Approved {queryset.count()} products.')

    approve_products.short_description = 'Approve selected products'
    
admin.site.register(Comment, CommentAdmin)
admin.site.register(Product)
admin.site.register(Category)