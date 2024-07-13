from django.contrib import admin
from django.contrib import messages
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_admin', 'is_manager')
    list_filter = ('is_active', 'is_admin', 'is_manager')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    actions = ['deactivate_users']

    def has_module_perms(self, request, obj=None):
        return request.user.is_admin

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) successfully deactivated.', messages.SUCCESS)

    deactivate_users.short_description = 'Deactivate selected users'

admin.site.register(User, UserAdmin)
