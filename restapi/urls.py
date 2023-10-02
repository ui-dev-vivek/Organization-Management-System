from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [    
    path('login/',login_api,name='login_api'),   
    path('clients/', ClientsApi.as_view(), name='client-registration'),
    path('clients/<str:username>/',ClientsApi.as_view(), name='client-registration-detail'),
    path('employees/', EmployeeApi.as_view(), name='employee-registration'),
    path('employees/<str:username>/', EmployeeApi.as_view(), name='employee-registration-detail'),
    path('organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('organizations/<str:slug>/', OrganizationDetailView.as_view(), name='organizations-data'),
    path('subsidiaries/', SubsidiariesListCreateView.as_view(), name='subsidiaries-list-create'),
    path('subsidiaries/<str:slug>/',SubsidiariesDetailView.as_view(), name='subsidiaries-detail'),
    path('subsidiaries/<str:slug>/projects/',SubsidiariesProjectsListView.as_view(), name='subsidiaries-projects-list'),
    path('subsidiaries/<slug:slug>/projects/budgets/',SubsidiariesDetailsView.as_view(), name='subsidiaries-projects-budgets-list'),
    path('projects/<int:project_id>/',ProjectDetailsWithEmployeeAndClientView.as_view(), name='projects-details'), 
     path('projects/', ProjectCreateView.as_view(), name='create-project'),   
    path('invoices/<str:invoice_number>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list'),
    path('payments/<str:transaction_id>/', PaymentDetailView.as_view(), name='payment-detailPaymentDetailView'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
] 
