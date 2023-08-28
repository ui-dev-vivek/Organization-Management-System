from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dotenv import dotenv_values
from django.contrib.auth import authenticate, login,logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from subsidiaries.models import Organizations
# from subsidiaries.models import Subsidiaries
from employees.models import Employees



from django.contrib import messages
# Create your views here.
ENV = dotenv_values('.env')


def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to your desired page after login
                if request.user.role=='employee':
                    subsidiary = request.user.employees.subsidiary
                elif request.user.role=='client':
                    subsidiary = request.user.employees.subsidiary
                else:
                    messages.error(request, 'You Have No Any Subsidiry')
                
                return redirect(subsidiary.slug+'/'+request.user.role)
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid Email/Username or Password.')  
    data = {
        'app_name': ENV.get('APP_NAME')
    }
    # Create a template named 'login.html'
    return render(request, 'auth/login.html', data)


def user_logout(request):
    # Perform logout logic
    # For example, using Django's built-in logout function:    
    auth_logout(request)   
    # Redirect to your desired page after logout
    return redirect('/')


@login_required
def subsidiaries(request):    
    user = request.user
    try:
        employee = Employees.objects.get(user=user)
        organization = employee.subsidiary.organization
        subsidiaries = organization.subsidiaries_set.all()
    except Employees.DoesNotExist:
        organization = None
        subsidiaries = []
    data = {
        'app_name': ENV.get('APP_NAME'),
        'organization':organization ,
        'subsidiaries':subsidiaries   
    }
    return render(request,'auth/subsidiaries.html',data);



