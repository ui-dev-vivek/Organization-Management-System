from django.shortcuts import HttpResponse, render,get_object_or_404,redirect
import os
from django.core.exceptions import ObjectDoesNotExist
from .decorators import is_employee
from subsidiaries.models import Subsidiaries
from projects.models import Projects,EmployeeOnProject
from django.http import request, JsonResponse
from employees.models import Employees
from PIL import Image
from django.contrib import messages
from authapp.models import User
from projects.models  import ProjectTask, Projects,TaskChecklist



@is_employee
def dashboard(request,subsidiary):    
    # logged_in_user=request.user
    # user_projects = Projects.objects.filter(employeeonproject__employees__user=logged_in_user)        
    return render(request,'employee/dashboard.html')

@is_employee
def emp_profile(request,subsidiary):
    user = request.user
    try:
        employee=Employees.objects.get(user=user)
    except Employees.DoesNotExist:
        messages.success(request, "Employee record not found for the user.")        
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

def project(request, subsidiary, slug):   
    employee_data = Employees.objects.get(user=request.user)  
    project = Projects.objects.get(slug=slug)
    userproject = EmployeeOnProject.objects.filter(employees=employee_data, project=project)
    allemployes = EmployeeOnProject.objects.select_related('employees__user').filter(project=project).all()
    members = []
    for employee in allemployes:
        employee_data = employee.employees
        user_data = employee_data.user
        employee_with_user = {
            "name": user_data.first_name + " " + user_data.last_name,            
            "employee_type": employee_data.get_emp_type_display,
            'is_lead':employee.is_lead,
            'profile_image':employee_data.profile_image.url        
        }     
        members.append(employee_with_user)
        
    project_tasks = ProjectTask.objects.filter(project=project)
    tasks_data = []

    for task in project_tasks:
        checklist_items = TaskChecklist.objects.filter(project_task=task)
        total_checklist_count = checklist_items.count()
        checked_count = checklist_items.filter(status=True).count()
        if(total_checklist_count !=0):
            progress=(checked_count/total_checklist_count)*100
        else:
            progress=0
        task_data = {
            'task': task,
            'checklist_items': checklist_items,
            'checked': checked_count,
            'taskchecklistcount': total_checklist_count,
            'progress':progress
        }
        tasks_data.append(task_data)
    data = {
        'project': project,
        'userproject': userproject,
        'members': members,
        'tasks_data':tasks_data
    }

    return render(request, 'employee/project.html', data)


@is_employee
def project_task_view(request, subsidiary):
    if request.method == 'POST':
        try:
            data = request.POST  # Assuming data is sent via POST form data

            # Assuming data includes project_id, title, description, and assigned_to_id
            project = data.get('project')
            title = data.get('title')
            description = data.get('description')
            

            # Assuming assigned_to_id is the ID of the assigned user
            
            end_date=data.get('end_date')
            # Assuming project_id is the ID of the associated project
            project = get_object_or_404(Projects, id=project)

            task = ProjectTask.objects.create(
                project=project,
                assigned_to=request.user,
                title=title,
                description=description,
                end_date=end_date
            )

            return JsonResponse({'task_id': task.title}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@is_employee
def update_project_task(request, subsidiary):    
    try:
        task = get_object_or_404(ProjectTask, uid=request.POST.get('task_id'))     
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.end_date = request.POST.get('end_date', task.end_date)
        task.save()

        # Get checklist items from the form
        checklist_ids=request.POST.getlist('checklist_id[]')
        titles = request.POST.getlist('titles[]')
        
        statuses = request.POST.getlist('status[]')       
        
        projecttask = get_object_or_404(ProjectTask, uid=request.POST.get('task_id'))
        
        # Update or insert TaskChecklist items
        for i in range(len(checklist_ids)-1):          
            
            if checklist_ids[i] != "no":                
                checklist_item = get_object_or_404(TaskChecklist, uid=checklist_ids[i] )
                checklist_item.title = titles[i]
                checklist_item.status = True if checklist_ids[i]  in statuses else False
                checklist_item.save()
                
            else:                
                # Insert new TaskChecklist item
                TaskChecklist.objects.create(
                    project_task=projecttask,
                    title=titles[i],
                    status=False
                )
        
        messages.success(request, "Task and checklist updated successfully.") 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        messages.error(request, "Falied To Create checklist.") 
    return redirect(request.META.get('HTTP_REFERER'))
    



# XHttp Methods. For JS
@is_employee
def upload_profile_image(request, subsidiary):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user 
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
        
        # Resize the image to 150x150 pixels
        img = Image.open(uploaded_image)        
        img = img.resize((150, 150), Image.ANTIALIAS)       
        resized_image_path = os.path.join('static/profile_images/', uploaded_image.name)
        img.save(resized_image_path)        
        employee.profile_image = resized_image_path
        employee.save()
        image_url = employee.profile_image.url
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Image not provided or invalid request.'}, status=400)
#code Closed!