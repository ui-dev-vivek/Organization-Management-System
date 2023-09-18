from django.contrib import admin
from .models import Projects, EmployeeOnProject, ClientOnProject,TaskChecklist,ProjectTask,Attachments


class EmployeeOnProjectForm(admin.StackedInline):
    model = EmployeeOnProject
    extra = 2    

class ClientOnProjectForm(admin.StackedInline):
    model = ClientOnProject
    extra = 1  
    max_num=1  
        

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'subsidiary', 'status']
    list_filter = ('subsidiary','status') 
    inlines=[EmployeeOnProjectForm,ClientOnProjectForm]
    search_fields = ['project_name', 'slug']
    prepopulated_fields = {'slug': ('project_name',)}    
    ordering = ['subsidiary__name']      
    autocomplete_fields = ['subsidiary']
    radio_fields={'status':admin.VERTICAL}


class EmployeeOnProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'employees', 'is_lead', 'assigned_date']
    list_filter = ['is_lead']
    search_fields = ['project__project_name', 'employees__name']
    ordering = ['subsidiary__name']      
    autocomplete_fields = ['employees']


class ClientOnProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'clients', 'assigned_date']
    search_fields = ['project__project_name', 'clients__name']
    ordering = ['subsidiary__name']      
    autocomplete_fields = ['clients']

admin.site.register(ProjectTask)
admin.site.register(TaskChecklist)
admin.site.register(Attachments)

# Code Cloded!