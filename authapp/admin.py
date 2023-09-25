from django.contrib import admin
from authapp.models import User, Address
from django.contrib.auth.admin import UserAdmin
from django import forms

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_employee', 'is_client')
    list_filter = ('is_employee', 'is_client')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('is_employee', 'is_client')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active','is_employee', 'is_client')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the User model with the admin site
admin.site.register(User, UserAdmin)


