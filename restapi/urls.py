from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [    
    path('login',login_api,name='login_api'),   
    path('client-registration/', ClientRegistration.as_view(), name='client-registration'),
    path('client-registration/<str:username>/',ClientRegistration.as_view(), name='client-registration-detail'),
    path('employee-registration/', EmployeeRegistration.as_view(), name='employee-registration'),
    path('employee-registration/<str:username>/', EmployeeRegistration.as_view(), name='employee-registration-detail'),
    path('organizations/', OrganizationListView.as_view(), name='org-list'),
    path('organization/', OrganizationDetailView.as_view(), name='org-data'),
    path('subsidiaries/', SubsidiariesListCreateView.as_view(), name='subsidiaries-list-create'),
    path('subsidiaries/<slug:slug>/',SubsidiariesDetailView.as_view(), name='subsidiaries-detail'),
    path('subsidiaries-projects/',SubsidiariesProjectsListView.as_view(), name='subsidiaries-projects-list'),
    path('subsidiaries-projects-budgets/',SubsidiariesDetailsView.as_view(), name='subsidiaries-projects-budgets-list'),
    path('projects-details/',ProjectDetailsWithEmployeeAndClientView.as_view(), name='projects-details'), 
    # path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),  
    path('invoices/<str:invoice_number>/', InvoiceAPIView.as_view(), name='invoice-detail'),
    path('invoices/', InvoiceAPIView.as_view(), name='invoice-list'),
    path('payment-history/', PaymentHistoryAPIView.as_view(), name='payment-history'),

] 




# Login : POST for Login  : DONE
# -------------------------------------------
# Client Registration:   POST    :Done
# Client Update By UserNAme :Done
# Get Client By UserName    :Done
# ----------------------------------------
# Employee Registration:  POST  :Done
# Employee Update :POST  : Done
# Get Employee By Username. :Done
# ------------------------------------------------
# Create Invoives 
# Update Invoices
# Get Invoices by invice_number
# ---------------------------------------------
# payment History Create
# payment Update
# get Payment by trx_id, or invoices _id
