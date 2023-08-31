from django.contrib import admin


from .models import Employees

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('get_user_name','get_organization_name', 'get_subsidiary_name', 'phone_no', 'emp_type')

    def get_organization_name(self, obj):
        return obj.subsidiary.organization.name
    get_organization_name.short_description = 'Organization Name'
    
    def get_user_name(self, obj):
        return obj.user.username
    get_user_name.short_description = 'User Name'


    def get_subsidiary_name(self, obj):
        return obj.subsidiary.name
    get_subsidiary_name.short_description = 'Subsidiary Name'

admin.site.register(Employees, EmployeesAdmin)
