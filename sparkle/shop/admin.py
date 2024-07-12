from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import Category, Product, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'content', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('content', 'author__email', 'product__title')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f'Approved {queryset.count()} comments.')

    approve_comments.short_description = 'Approve selected comments'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_approved', 'date_created')
    list_filter = ('is_approved', 'category')
    search_fields = ('title', 'description', 'slug')
    actions = ['approve_products']

    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'Approved {queryset.count()} products.')

    approve_products.short_description = 'Approve selected products'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_sub', 'slug')
    list_filter = ('is_sub',)
    search_fields = ('title', 'slug')

# Register your models here
admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
