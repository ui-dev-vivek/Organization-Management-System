from django.shortcuts import HttpResponse, render
import os
from .decorators import is_client
from subsidiaries.models import Subsidiaries
from clients.models import Clients
from django.http import HttpResponseBase, request, JsonResponse
from projects.models import Projects,EmployeeOnProject,ClientOnProject
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

    data = {
        'project': project,
        'clientproject': clientproject,
        'members': members
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
            if user.address.exists():  
                address = user.address.first()  
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
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user 
        try:
            clients = Clients.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Employee record not found for the user.'}, status=400)

     
        if clients.profile_image:
            old_image_path = clients.profile_image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        uploaded_image = request.FILES['profile_image']

        img = Image.open(uploaded_image)

        img = img.resize((150, 150), Image.ANTIALIAS)

        resized_image_path = os.path.join('static/profile_images/', uploaded_image.name)
        img.save(resized_image_path)

        clients.profile_image = resized_image_path
        clients.save()

        image_url = clients.profile_image.url
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Image not provided or invalid request.'}, status=400)
#code Close!