from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price', 'quantity', 'get_cost')
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'updated', 'status', 'shipping_price', 'get_total_price')
    list_filter = ('status', 'created', 'user')
    search_fields = ('user__email', 'user__full_name')
    actions = ['mark_as_completed']
    inlines = [OrderItemInline]
    
    def get_total_price(self, obj):
        return obj.get_total_price
    get_total_price.short_description = 'Total Price'

    def mark_as_completed(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f'Marked {queryset.count()} orders as completed.')

    mark_as_completed.short_description = 'Mark selected orders as completed'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'get_cost')
    list_filter = ('order', 'product')
    search_fields = ('order__user__email', 'product__title')
    
    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Cost'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
