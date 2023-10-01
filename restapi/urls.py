from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [    
    path('login',login_api,name='login_api'),   
    path('client-registration/', ClientRegistration.as_view(), name='client-registration'),
    path('client-registration/<str:username>/',ClientRegistration.as_view(), name='client-registration-detail'),
    path('employee-registration/', EmployeeRegistration.as_view(), name='employee-registration'),
    path('employee-registration/<str:username>/', EmployeeRegistration.as_view(), name='employee-registration-detail'),
    path('organizations/', OrganizationListView.as_view(), name='organizations-list'),
    path('organization/', OrganizationDetailView.as_view(), name='organizations-data'),
    path('subsidiaries/', SubsidiariesListCreateView.as_view(), name='subsidiaries-list-create'),
    path('subsidiaries/<slug:slug>/',SubsidiariesDetailView.as_view(), name='subsidiaries-detail'),
    path('subsidiaries-projects/',SubsidiariesProjectsListView.as_view(), name='subsidiaries-projects-list'),
    path('subsidiaries-projects-budgets/',SubsidiariesDetailsView.as_view(), name='subsidiaries-projects-budgets-list'),
    path('projects-details/',ProjectDetailsWithEmployeeAndClientView.as_view(), name='projects-details'),    
    path('invoices/<str:invoice_number>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list'),
    path('payments/<str:transaction_id>/', PaymentDetailView.as_view(), name='payment-detailPaymentDetailView'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
] 
