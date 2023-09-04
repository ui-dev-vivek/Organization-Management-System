from django.shortcuts import HttpResponse, render
import os
from django.core.exceptions import ObjectDoesNotExist
from .decorators import is_employee
from subsidiaries.models import Subsidiaries
from projects.models import Projects,EmployeeOnProject
from django.http import request, JsonResponse
from employees.models import Employees
from PIL import Image
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt


@is_employee
def dashboard(request,subsidiary):
    print(request)
    logged_in_user=request.user
    # user_projects = Projects.objects.filter(employeeonproject__employees__user=logged_in_user)
        
    return render(request,'employee/dashboard.html')

@is_employee
def emp_profile(request,subsidiary):
    user = request.user
    try:
        employee=Employees.objects.get(user=user)
    except Employees.DoesNotExist:
        print('employe record not found')
        # return render(request,'error.html',{'error_message': 'Employee record not found for the user.'});
    if request.method=='POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "Profile updated successfully.")
        
    data={
        'user':request.user
    }
    return render(request,'employee/profile.html',data)

def project(request,subsidiary,slug):
    
    employee_data = Employees.objects.get(user=request.user)

    
    project=Projects.objects.get(slug=slug)
    userproject = EmployeeOnProject.objects.filter(employees=employee_data,project=project)
    data={
        'project':project,
        'userproject':userproject
    }
    return render(request,'employee/project.html',data)



# XHttp Methods.
def upload_profile_image(request, subsidiary):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user  # Assuming you're using authentication to identify the user.
        try:
            employee = Employees.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Employee record not found for the user.'}, status=400)

        # Delete the old profile image if it exists
        if employee.profile_image:
            old_image_path = employee.profile_image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        uploaded_image = request.FILES['profile_image']

        # Open the image
        img = Image.open(uploaded_image)

        # Resize the image to 150x150 pixels
        img = img.resize((150, 150), Image.ANTIALIAS)

        # Save the resized image
        resized_image_path = os.path.join('static/profile_images/', uploaded_image.name)
        img.save(resized_image_path)

        # Set the new profile image
        employee.profile_image = resized_image_path
        employee.save()

        image_url = employee.profile_image.url
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Image not provided or invalid request.'}, status=400)