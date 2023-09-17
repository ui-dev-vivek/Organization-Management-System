from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [    
    path('login',login_api,name='login_api'),
    path('organizations/', OrganizationListView.as_view(), name='org-list'),
    path('organization/', OrganizationDetailView.as_view(), name='org-data'),
    path('subsidiaries/', SubsidiariesListCreateView.as_view(), name='subsidiaries-list-create'),
    path('subsidiaries/<slug:slug>/',SubsidiariesDetailView.as_view(), name='subsidiaries-detail'),
    path('subsidiaries-projects/',SubsidiariesProjectsListView.as_view(), name='subsidiaries-projects-list'),
    path('subsidiaries-projects-budgets/',SubsidiariesDetailsView.as_view(), name='subsidiaries-projects-budgets-list'),
    path('projects-details/',ProjectDetailsWithEmployeeAndClientView.as_view(), name='projects-details'), 
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
   

]