from django.contrib import admin
from .models import Projects, EmployeeOnProject, ClientOnProject

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'subsidiary', 'status']
    list_filter = ['status']
    search_fields = ['project_name', 'slug']
    prepopulated_fields = {'slug': ('project_name',)}

@admin.register(EmployeeOnProject)
class EmployeeOnProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'employees', 'is_lead', 'assigned_date']
    list_filter = ['is_lead']
    search_fields = ['project__project_name', 'employees__name']

@admin.register(ClientOnProject)
class ClientOnProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'clients', 'assigned_date']
    search_fields = ['project__project_name', 'clients__name']



