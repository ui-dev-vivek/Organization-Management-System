from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

def dashboard(request,subsidiary):  
    print(subsidiary)
    return HttpResponse(request.user.username)
