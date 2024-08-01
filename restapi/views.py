from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import generics,permissions
from employees.models import Employees
from clients.models import Clients
from authapp.models import User,Address
from projects.models import Projects
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from subsidiaries.models import Organizations,Subsidiaries,Budgets
from django.http import JsonResponse,Http404
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from restapi.permission import AdminAction
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
# For Login
@api_view(['POST']) 
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # login(request, user)
        return Response({'message': 'Authentication successful','status':'success', 'username': user.username})
    else:
        return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

class SubsidiariesListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]
    queryset = Subsidiaries.objects.all()
    serializer_class = SubsidiarySerializer
    def create(self, request, *args, **kwargs):        
        return Response({"message": "Method not allowed for creating subsidiaries"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SubsidiariesDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, AdminAction]

    def get_object(self):
        slug = self.kwargs.get('slug')
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        return subsidiary

    def get(self, request, slug, format=None):
        instance = self.get_object()
        serializer = SubsidiarySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrganizationListView(ListAPIView):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]    

    def get_queryset(self):
        organizations = super().get_queryset()
        for organization in organizations:
            organization.subsidiaries = Subsidiaries.objects.filter(organization=organization)
            for subsidiary in organization.subsidiaries:
                subsidiary.budgets = Budgets.objects.filter(subsidiary=subsidiary)
        return organizations

class OrganizationDetailView(ListAPIView):
    serializer_class = OrganizationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        # slug = self.request.query_params.get('slug', None)
        if slug:
            organizations = Organizations.objects.filter(slug=slug).all()
            for organization in organizations:
                organization.subsidiaries = Subsidiaries.objects.filter(organization=organization)
                for subsidiary in organization.subsidiaries:
                    subsidiary.budgets = Budgets.objects.filter(subsidiary=subsidiary)
            return organizations
        else:
            return Organizations.objects.none()

class SubsidiariesProjectsListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]

    def get(self, request, slug, format=None):
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        projects = Projects.objects.filter(subsidiary=subsidiary)
        
        subsidiary_serializer = SubsidiariesSerializer(subsidiary)
        projects_serializer = ProjectsSerializer(projects, many=True)        
        response_data = {
            "subsidiary": subsidiary_serializer.data,
            "projects": projects_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class SubsidiariesDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]

    def get(self, request, slug, format=None):
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        projects = Projects.objects.filter(subsidiary=subsidiary)
        projects_serializer = ProjectsSerializer(projects, many=True)
        budgets = Budgets.objects.filter(subsidiary=subsidiary)
        budgets_serializer = BudgetSerializer(budgets, many=True)
        response_data = {
            "subsidiary": SubsidiariesSerializer(subsidiary).data,
            "projects": projects_serializer.data,
            "budgets": budgets_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)  

class ProjectDetailsWithEmployeeAndClientView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]

    def get(self, request, project_id, path=None, format=None):
        if project_id is not None:
            instance = get_object_or_404(Projects, id=project_id)

            # Retrieve employees associated with the project
            employees = EmployeeOnProject.objects.filter(project=instance)
            employee_data = [
                {
                    "employee_id": emp.employees.uid,
                    "user_data": {
                        "email": emp.employees.user.email,
                        "username": emp.employees.user.username,
                        "first_name": emp.employees.user.first_name,
                        "last_name": emp.employees.user.last_name,
                    },
                    "phone_no": emp.employees.phone_no,
                    "emp_type": emp.employees.emp_type,
                    'is_lead':emp.is_lead,
                    'assigned_date':emp.assigned_date,
                }
                for emp in employees
            ]

            # Retrieve clients associated with the project
            clients = ClientOnProject.objects.filter(project=instance)
            client_data = [
                {
                    "client_id": client.clients.uid,
                    "user_data": {
                        "email": client.clients.user.email,
                        "username": client.clients.user.username,
                        "first_name": client.clients.user.first_name,
                        "last_name": client.clients.user.last_name,
                    },
                    "phone_no": client.clients.phone_no,
                    "organization_name": client.clients.organization_name,
                    'assigned_date':client.assigned_date,
                    
                }
                for client in clients
            ]

            # Prepare the final response
            response_data = {
                "project_details": {
                    "project_name": instance.project_name,
                    "project_desc": instance.project_desc,
                    "start_date": instance.start_date,
                    "end_date": instance.end_date,
                    "status": instance.status,
                },
                "employees": employee_data,
                "clients": client_data,
            }

            return Response(response_data)
        else:
            return Response({"error": "parameter is missing"})  
 
class ProjectCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]
    
    def put(self, request, format=None):
        slug= request.data.get('slug')
        project = get_object_or_404(Projects, slug=slug)
        serializer = ProjectsSerializer(project, data=request.data)

        if serializer.is_valid():
            inst=serializer.save()
            response_data = {
                    'uid': inst.id,
                    'slug': inst.slug,
                    'message': 'Project Updated successfully.'
                }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            inst=serializer.save()
            response_data = {
                    'uid': inst.id,
                    'slug': inst.slug,
                    'message': 'Project created successfully.'
                }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
    
class InvoiceDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]
    def delete(self,request, invoice_number, format=None):        
        try:
            invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
            invoice.delete()
            return Response({"message": "Invoice Deleted successfully"}, status=status.HTTP_200_OK)            
        except User.DoesNotExist:
            return Response({"message": "Invoices Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, invoice_number, format=None):
        invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
        invoices_inst = InvoiceGetSerializer(invoice)
        user_serializer = UserSerializer(invoice.user) 
        payment_history = PaymentHistory.objects.filter(invoice=invoice)
        if payment_history.exists():
            payment_serializer = PaymentHistorySerializer(payment_history, many=True)
        else:
            payment_serializer = []
        response_data = {
            'user': user_serializer.data,
            'invoices': invoices_inst.data if invoices_inst else None,
            'payments': payment_serializer.data if payment_serializer else None
        }
        return Response(response_data)

class InvoiceListCreateView(APIView):
    def put(self, request, format=None):        
        invoice_number = request.data.get('invoice_number', '')
        invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()            
            response_data = {
                    'uid': invoice.uid,
                    'invoice_number': invoice.invoice_number,
                    'message': 'Invoice Update successfully.'
                }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        try:
            data = request.data
            items_data = data.pop('items', [])  
            serializer = InvoiceSerializer(data=data)
            if serializer.is_valid():
                invoice = serializer.save()               
                for item_data in items_data:
                    Item.objects.create(invoice=invoice, **item_data)
                response_data = {
                    'uid': invoice.uid,
                    'invoice_number': invoice.invoice_number,
                    'message': 'Invoice created successfully.'
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = {
                'message': f'An error occurred: {str(e)}'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
class PaymentDetailView(APIView):
    def get(self, request, transaction_id, format=None):
        try:
            payment = get_object_or_404(PaymentHistory, transaction_id=transaction_id)
            payment_serializer = PaymentHistorySerializer(payment)
            user_serializer = UserSerializer(payment.user)
            try:
                invoice = payment.invoice
                invoice_serializer = InvoiceSerializer(invoice)
            except Invoice.DoesNotExist:
                invoice_serializer = None

            response_data = {
                'user': user_serializer.data if user_serializer else None,
                'invoice': invoice_serializer.data if invoice_serializer else None,
                'payment': payment_serializer.data if payment_serializer else None
            }
            return Response(response_data)
        except PaymentHistory.DoesNotExist:
            return Response({'error': 'PaymentHistory not found'}, status=status.HTTP_404_NOT_FOUND)

class PaymentListCreateView(APIView):
    def put(self, request, format=None):
        transaction_id=request.data.get('transaction_id');
        try:           
            payment = get_object_or_404(PaymentHistory, transaction_id=transaction_id)
            serializer = PaymentHistorySerializer(payment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'uid': payment.uid,
                    'transaction_id': payment.transaction_id,
                    'message': 'Payment Update successfully.'
                }
                return Response(response_data, status=status.HTTP_201_CREATED)                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PaymentHistory.DoesNotExist:
            return Response({'error': 'PaymentHistory not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = PaymentHistorySerializer(data=request.data)

        if serializer.is_valid():
            payment = serializer.save()  # Save the new PaymentHistory object
            response_data = {
                'uid': payment.uid,  # Assuming PaymentHistory has a UID field
                'transaction_id': payment.transaction_id,  # Assuming PaymentHistory has a transaction_id field
                'message': 'Payment created successfully.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientsApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction] 

    def get(self, request, username, format=None):
        try:
            user_instance = User.objects.get(username=username)
            if not user_instance.is_client:
                return Response({"message": "Client Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            client_instance = Clients.objects.get(user=user_instance)
            client_serializer = ClientRegSerializer(client_instance)
        except Clients.DoesNotExist:
            client_serializer = None

        try:
            address_instance = Address.objects.get(user=user_instance)
            address_serializer = AddressSerializer(address_instance)
        except Address.DoesNotExist:
            address_serializer = None

        user_serializer = UserRegSerializer(user_instance)

        response_data = {
            "user": user_serializer.data,
            "client": client_serializer.data if client_serializer else None,
            "address": address_serializer.data if address_serializer else None
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request,username, format=None):        
        try:
            user_instance = User.objects.get(username=username)
            if user_instance.is_client:
                user_instance.delete()
                return Response({"message": "Client Deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Not a client"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Client Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        request_data = request.data.copy()
        try:
            user_data = request_data.get('user')
            if user_data:
                user_data['is_client'] = True
                user_data['password'] = make_password(user_data['password'])  # Encrypt password
            else:
                return Response({'error': 'User data not found!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return self.create_or_update(request, create=True)

    def put(self, request, format=None):
        return self.create_or_update(request, create=False)

    def create_or_update(self, request, create=True):
        # Extract username from the request
        username = request.data.get('user', {}).get('username', '')

        try:
            user_instance = User.objects.get(username=username)
        except User.DoesNotExist:
            user_instance = None

        if create or user_instance is None:
            user_serializer = UserRegSerializer(data=request.data.get('user', {}))
        else:
            user_data = request.data.get('user', {})
            user_data['password'] = make_password(user_data.get('password'))
            user_serializer = UserRegSerializer(user_instance, data=user_data, partial=True)

        if user_serializer.is_valid():
            user_instance = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_data = request.data.get('client', {})
        client_data['user'] = user_instance.id

        try:
            client_instance = Clients.objects.get(user=user_instance)
            client_serializer = ClientRegSerializer(client_instance, data=client_data, partial=True)
        except Clients.DoesNotExist:
            client_instance = None
            client_serializer = ClientRegSerializer(data=client_data)

        if client_serializer.is_valid():
            client_instance = client_serializer.save()
        else:
            user_instance.delete()
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Address data if it exists
        address_data = request.data.get('address', {})
        address_data['user'] = user_instance.id

        try:
            address_instance = Address.objects.get(user=user_instance)
            address_serializer = AddressSerializer(address_instance, data=address_data, partial=True)
        except Address.DoesNotExist:
            address_instance = None
            address_serializer = AddressSerializer(data=address_data)

        if address_serializer.is_valid():
            address_instance = address_serializer.save()
        else:
            user_instance.delete()
            client_instance.delete()
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if create:
            return Response({"message": "Client registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Client information updated successfully"}, status=status.HTTP_200_OK)          

class EmployeeApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,AdminAction]
    def get(self,request,username,formate=None):
        try:
            user_instance = User.objects.get(username=username)
            if not user_instance.is_employee:
                return Response({"message": "Employee Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            employee_instance = Employees.objects.get(user=user_instance)
            employee_serializer = EmployeeRegSerializer(employee_instance)
        except Employees.DoesNotExist:
            employee_serializer = None            
        try:
            address_instance = Address.objects.get(user=user_instance)
            address_serializer = AddressSerializer(address_instance)
        except Address.DoesNotExist:
            address_serializer = None

        user_serializer = UserSerializer(user_instance)

        response_data = {
            "user": user_serializer.data,
            "employee": employee_serializer.data if employee_serializer else None,
            "address": address_serializer.data if address_serializer else None
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def delete(self, request,username,format=None):       
        try:
            user_instance = User.objects.get(username=username)
            if user_instance.is_employee:
                user_instance.delete()
                return Response({"message": "Employee Deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Not an Employee."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Employee Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, format=None):        
        request_data = request.data.copy()
        user_data = request_data.get('user', {})        
        if 'password' in user_data:
            user_data['password'] = make_password(user_data['password'])

        user_data['is_employee'] = True
        return self.create_or_update(request, create=True)

    def put(self, request, format=None):
        return self.create_or_update(request, create=False)

    def create_or_update(self, request, create=True):
        # Extract username from the request
        username = request.data.get('user', {}).get('username', '')

        try:
            user_instance = User.objects.get(username=username)
        except User.DoesNotExist:
            user_instance = None
        
        if create or user_instance is None:
            user_serializer = UserRegSerializer(data=request.data.get('user', {}))
        else:            
            user_serializer = UserRegSerializer(user_instance, data=request.data.get('user', {}), partial=True)

        if user_serializer.is_valid():
            user_instance = user_serializer.save()
        else:            
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Client data if it exists
        employee_data = request.data.get('employee', {})
        employee_data['user'] = user_instance.id

        try:
            employee_instance = Employees.objects.get(user=user_instance)
            employee_serializer = EmployeeRegSerializer(employee_instance, data=employee_data, partial=True)
        except Employees.DoesNotExist:
            employee_instance = None
            employee_serializer = EmployeeRegSerializer(data=employee_data)

        if employee_serializer.is_valid():
            employee_instance = employee_serializer.save()
        else:
            user_instance.delete()
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Address data if it exists
        address_data = request.data.get('address', {})
        address_data['user'] = user_instance.id

        try:
            address_instance = Address.objects.get(user=user_instance)
            address_serializer = AddressSerializer(address_instance, data=address_data, partial=True)
        except Address.DoesNotExist:
            address_instance = None
            address_serializer = AddressSerializer(data=address_data)

        if address_serializer.is_valid():
            address_instance = address_serializer.save()
        else:
            user_instance.delete()
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if create:
            return Response({"message": "Employee registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Employee information updated successfully"}, status=status.HTTP_200_OK)
    
  