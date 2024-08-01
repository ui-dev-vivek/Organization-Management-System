from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('' , dashboard, name="dashboard" ),
    path('profile',emp_profile,name='emp.profile'),
    path('upload_profile_image/', upload_profile_image, name='upload_profile_image'),
    path('project/<str:slug>',project,name='emp.project'),
    path('project-task/',project_task_view,name='project_task'),
    path('update-project-task/',update_project_task,name="update_project_task"),
    path('project_task/<str:task_id>/delete/', delete_project_task, name='delete_project_task'),
    path('project_task_checklist/<str:task_id>/delete/', delete_project_task_checklist, name='delete_project_task_checklist'),
    path('upload_attachment/', upload_attachment, name='upload_attachment'),
    path('attachment/<str:task_id>/delete/', delete_attachment, name='delete_attachment'),
]



