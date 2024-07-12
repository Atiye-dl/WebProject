from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_admin', 'is_manager')
    list_filter = ('is_active', 'is_admin', 'is_manager')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    def has_module_perms(self, request, obj=None):
        return request.user.is_admin

admin.site.register(User, UserAdmin)
