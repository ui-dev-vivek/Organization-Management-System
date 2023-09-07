from django.shortcuts import HttpResponse, render
from .decorators import is_client
from subsidiaries.models import Subsidiaries


@is_client
def dashboard(request,subsidiary):       
    return render(request,'client/dashboard.html')

@is_client
def client_profile(request,subsidiary):
    return HttpResponse('Profile')
    