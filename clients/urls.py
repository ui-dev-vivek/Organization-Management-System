from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [
    path('' , dashboard, name="dashboard" ),
    path('profile',client_profile,name="client_profile"),
    path('upload_profile_image/', upload_profile_image, name='client_upload_profile_image'),
    path('project/<str:slug>',project,name='client_project'),
    path('invoice/',invoices,name="client_invoices"),
    # path('invoice<id:uid>',invoice_by_id,name="client_invoices_id")
]

