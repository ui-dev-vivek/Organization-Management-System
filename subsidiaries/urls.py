from django.urls import path, include
from .views import *
urlpatterns = [
    # path('', subsidiary_list,name="subsidiary-list"),
    path('client/', include('clients.urls')),
    path('employee/', include('employees.urls')),
]
