from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [
    path('employee' , EmployeeList.as_view(), name="employees" ),
    path('login',login_api,name='login_api')
]