from django.shortcuts import HttpResponse, render
from .decorators import is_employee
from subsidiaries.models import Subsidiaries


@is_employee
def dashboard(request,subsidiary):       
    return render(request,'employee/dashboard.html')