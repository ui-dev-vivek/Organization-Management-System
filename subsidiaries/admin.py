from django.contrib import admin
from .models import Organizations, Subsidiaries, Budgets
from django.contrib import messages


class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'created_at', 'updated_at')
    search_fields = ['name', 'description'] 
    ordering = ['name']  

class SubsidiariesAdmin(admin.ModelAdmin):
    list_display = ('name','organization', 'slug', 'description', 'created_at', 'updated_at')
    search_fields = ['name', 'description']  
    ordering = ['name']     
    autocomplete_fields = ['organization']

class BudgetsAdmin(admin.ModelAdmin):
    list_display = ('subsidiary', 'year', 'amount',)
    search_fields = ['year'] 
    ordering = ['year'] 
    list_filter = ('subsidiary','year',)  
    autocomplete_fields = ['subsidiary']
    
    def save_model(self, request, obj, form, change):       
        existing_budget = Budgets.objects.filter(year=obj.year, subsidiary=obj.subsidiary).first()
        if existing_budget and existing_budget.pk != obj.pk:
            messages.error(request, 'A budget for this year and subsidiary already exists.')
            return

        super().save_model(request, obj, form, change)

admin.site.register(Organizations, OrganizationsAdmin)
admin.site.register(Subsidiaries, SubsidiariesAdmin)
admin.site.register(Budgets, BudgetsAdmin)

# Code Closed!