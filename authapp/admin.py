from django.contrib import admin
from authapp.models import User,Address
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# admin.site.register(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','is_employee', 'is_client', 'is_staff', 'is_superuser')
    list_filter = ('is_employee', 'is_client', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'is_employee', 'is_client')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(Address)