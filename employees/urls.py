from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [
    path('' , dashboard, name="dashboard" ),
    path('profile',emp_profile,name='emp.profile'),
    path('upload_profile_image/', upload_profile_image, name='upload_profile_image'),
    path('project/<str:slug>',project,name='emp.project'),
]