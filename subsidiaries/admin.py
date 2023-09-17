from django.contrib import admin
from .models import Organizations, Subsidiaries,Budgets
# Register your models here.
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','description', 'created_at', 'updated_at')
    
class SubsidiariesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','description', 'created_at', 'updated_at')

admin.site.register(Organizations,OrganizationsAdmin)
admin.site.register(Subsidiaries,SubsidiariesAdmin)
admin.site.register(Budgets)