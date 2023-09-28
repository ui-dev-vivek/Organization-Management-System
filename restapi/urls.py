from django.contrib import admin
from django.urls import path,include

from .views import *

urlpatterns = [    
    path('login',login_api,name='login_api'),   
    path('client-registration/', ClientRegistration.as_view(), name='client-registration'),
    path('employee-registration/', EmployeeRegistration.as_view(), name='employee-registration'),
    path('organizations/', OrganizationListView.as_view(), name='org-list'),
    path('organization/', OrganizationDetailView.as_view(), name='org-data'),
    path('subsidiaries/', SubsidiariesListCreateView.as_view(), name='subsidiaries-list-create'),
    path('subsidiaries/<slug:slug>/',SubsidiariesDetailView.as_view(), name='subsidiaries-detail'),
    path('subsidiaries-projects/',SubsidiariesProjectsListView.as_view(), name='subsidiaries-projects-list'),
    path('subsidiaries-projects-budgets/',SubsidiariesDetailsView.as_view(), name='subsidiaries-projects-budgets-list'),
    path('projects-details/',ProjectDetailsWithEmployeeAndClientView.as_view(), name='projects-details'), 
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),  
    path('payment-history/', PaymentHistoryAPIView.as_view(), name='payment-history'),

] 




# Login : POST for Login  : DONE
# -------------------------------------------
# Client Registration:   POST    :Done
# Client Update By UserNAme
# Get Client By UserName
# ----------------------------------------
# Employee Registration:  POST  :DOne
# Employee Update :POST
# Get Employee By Username.
# ------------------------------------------------
# Create Invoives
# Update Invoices
# Get Invoices by invice_number
# ---------------------------------------------
# payment History Create
# payment Update
# get Payment by trx_id, or invoices _id
