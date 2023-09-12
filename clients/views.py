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
    # try:
    #     client=Client.objects.get(user=user)
    # except client.DoesNotExist:
    #     print('clients record not found')
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
    return render(request,'client/profile.html',data)

def project(request, subsidiary, slug):
    # Assuming you have the necessary imports
    
    # Fetch the currently logged-in employee
    client_data = Clients.objects.get(user=request.user)
    

    # Fetch the project with the specified slug
    project = Projects.objects.get(slug=slug)

    # Fetch the user's association with the project
    clientproject = ClientOnProject.objects.filter(clients=client_data, project=project)

    # Fetch all employees associated with the project and related user data
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
            # Add more user-related fields as needed
        }

        # Append the combined data to the list
        members.append(employee_with_user)

    data = {
        'project': project,
        'clientproject': clientproject,
        'members': members
    }

    return render(request, 'client/project.html', data)

@is_client
def invoices(request, subsidiary):
    user = request.user  # You may need to adjust this based on your authentication setup

    if user.is_authenticated:
        # Retrieve all invoices for the user
        invoices = Invoice.objects.filter(user=user)
       
        # Serialize invoice data
        serialized_invoices = []
        for invoice in invoices:
            invoice_data = {
                'invoice_number': invoice.invoice_number,
                'amount': invoice.amount,
                'is_paid': invoice.is_paid,
                'due_date': invoice.due_date,
                'payment_method': invoice.payment_method,
                'tax_rate': invoice.tax_rate,
                # Add other fields you need here
            }

            # Add user details
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                # Add other user fields you need here
            }
            invoice_data['user'] = user_data

            # Add address details
            if user.address.exists():  # Assuming you have a related name 'address' on the User model
                address = user.address.first()  # Get the first address associated with the user
                address_data = {
                    'street_address': address.street_address,
                    'apt_suite_number': address.apt_suite_number,
                    'city': address.city,
                    'state': address.state,
                    'zip_code': address.zip_code,
                    'country': address.country,
                    # Add other address fields you need here
                }
                invoice_data['address'] = address_data

            # Add items for the invoice
            items = Item.objects.filter(invoice=invoice)
            item_data = []
            for item in items:
                item_data.append({
                    'name': item.name,
                    'description': item.description,
                    'unit_price': item.unit_price,
                    'quantity': item.quantity,
                    # Add other item fields you need here
                })
            invoice_data['items'] = item_data

            # Add payment history for the invoice
            payment_history = PaymentHistory.objects.filter(invoice=invoice)
            payment_data = []
            for payment in payment_history:
                payment_data.append({
                    'amount': payment.amount,
                    'payment_date': payment.payment_date,
                    'payment_method': payment.payment_method,
                    'transaction_id': payment.transaction_id,
                    # Add other payment history fields you need here
                })
            invoice_data['payment_history'] = payment_data

            serialized_invoices.append(invoice_data)
            # print(serialized_invoices)
    
    return render(request,'client/invoices.html',{'invoices': serialized_invoices})
    

# XHttp Methods.
def upload_profile_image(request, subsidiary):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user  # Assuming you're using authentication to identify the user.
        try:
            clients = Clients.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Employee record not found for the user.'}, status=400)

        # Delete the old profile image if it exists
        if clients.profile_image:
            old_image_path = clients.profile_image.path
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
        clients.profile_image = resized_image_path
        clients.save()

        image_url = clients.profile_image.url
        return JsonResponse({'image_url': image_url})
    else:
        return JsonResponse({'error': 'Image not provided or invalid request.'}, status=400)