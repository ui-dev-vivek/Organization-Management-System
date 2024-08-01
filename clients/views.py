from django.shortcuts import HttpResponse, render
import os
from django.conf import settings
from .decorators import is_client
from subsidiaries.models import Subsidiaries
from clients.models import Clients
from django.http import HttpResponseBase, request, JsonResponse
from projects.models import Projects,EmployeeOnProject,ClientOnProject,TaskChecklist,Attachments,ProjectTask

from payments.models import Invoice,PaymentHistory,Item
from django.contrib import messages
from PIL import Image

@is_client
def dashboard(request,subsidiary):    
    return render(request,'client/dashboard.html')

@is_client
def client_profile(request,subsidiary):    
    user = request.user   
    if request.method=='POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, "Profile updated successfully.")
        
    data={
        'user':request.user
    }
    return render(request,'client/profile.html',data)
@is_client
def project(request, subsidiary, slug):
    client_data = Clients.objects.get(user=request.user)
    project = Projects.objects.get(slug=slug)
    clientproject = ClientOnProject.objects.filter(clients=client_data, project=project)
    allemployes = EmployeeOnProject.objects.select_related('employees__user').filter(project=project).all()

    members = []

    for employee in allemployes:
        employee_data = employee.employees
        user_data = employee_data.user

        # Combine employee data with user data
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
        if total_checklist_count != 0:
            progress = (checked_count / total_checklist_count) * 100
        else:
            progress = 0
        task_data = {
            "task": task,
            "checklist_items": checklist_items,
            "checked": checked_count,
            "taskchecklistcount": total_checklist_count,
            "progress": progress,
        }
        tasks_data.append(task_data)
        
    attachments = Attachments.objects.filter(project=project)

    attachment_data = []
    for attachment in attachments:
        attachment_data.append({
            'id': attachment.uid,
            'file_name': attachment.file_name,
            'attachment_file': attachment.attachment_file.url.split("/")[-1]
        })

    data = {
        'project': project,
        'clientproject': clientproject,
        'members': members,
        "tasks_data": tasks_data,
        "attachments":attachment_data
    }

    return render(request, 'client/project.html', data)

@is_client
def invoices(request, subsidiary):
    user = request.user  
    if user.is_authenticated:
        invoices = Invoice.objects.filter(user=user)
        serialized_invoices = []
        for invoice in invoices:
            invoice_data = {
                'invoice_number': invoice.invoice_number,
                'amount': invoice.amount,
                'is_paid': invoice.is_paid,
                'due_date': invoice.due_date,
                'payment_method': invoice.payment_method,
                'tax_rate': invoice.tax_rate,                
            }
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,               
            }
            invoice_data['user'] = user_data           
            if user.address:  
                address = user.address 
                address_data = {
                    'street_address': address.street_address,
                    'apt_suite_number': address.apt_suite_number,
                    'city': address.city,
                    'state': address.state,
                    'zip_code': address.zip_code,
                    'country': address.country,                    
                }
                invoice_data['address'] = address_data
            
            items = Item.objects.filter(invoice=invoice)
            item_data = []
            for item in items:
                item_data.append({
                    'name': item.name,
                    'description': item.description,
                    'unit_price': item.unit_price,
                    'quantity': item.quantity,
                    
                })
            invoice_data['items'] = item_data
            
            payment_history = PaymentHistory.objects.filter(invoice=invoice)
            payment_data = []
            for payment in payment_history:
                payment_data.append({
                    'amount': payment.amount,
                    'payment_date': payment.payment_date,
                    'payment_method': payment.payment_method,
                    'transaction_id': payment.transaction_id,
                    
                })
            invoice_data['payment_history'] = payment_data
            serialized_invoices.append(invoice_data)
    
    return render(request,'client/invoices.html',{'invoices': serialized_invoices})
    

# XHttp Methods.
@is_client
def upload_profile_image(request, subsidiary):
    if request.method == "POST" and request.FILES.get("profile_image"):
        user = request.user
        try:
            client = Clients.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Client record not found for the user."}, status=400
            )

       
        if client.profile_image:
            old_image_path = os.path.join(settings.MEDIA_ROOT, str(client.profile_image.url))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        uploaded_image = request.FILES["profile_image"]

        
        img = Image.open(uploaded_image)
        img = img.resize((150, 150), Image.ANTIALIAS)

       
        resized_image_path = os.path.join("profile_images", uploaded_image.name)

       
        resized_image_full_path = os.path.join(settings.MEDIA_ROOT, resized_image_path)
        img.save(resized_image_full_path)

        client.profile_image = resized_image_path
        client.save()

        
        image_url = os.path.join(settings.MEDIA_URL, resized_image_path)
        return JsonResponse({"image_url": image_url})
    else:
        return JsonResponse(
            {"error": "Image not provided or invalid request."}, status=400
        )

#code Close!