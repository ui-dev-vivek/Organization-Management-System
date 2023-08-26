from django.shortcuts import render, redirect
from dotenv import dotenv_values
from django.contrib.auth import authenticate, login,logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages
# Create your views here.
ENV = dotenv_values('.env')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to your desired page after login
                return redirect('/subsidiaries')
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