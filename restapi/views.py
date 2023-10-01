from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import generics,permissions
from employees.models import Employees
from clients.models import Clients
from authapp.models import User,Address
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
from django.shortcuts import get_object_or_404

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


# To return all subsidiaries list
class SubsidiariesListCreateView(generics.ListCreateAPIView):
    queryset = Subsidiaries.objects.all()
    serializer_class = SubsidiarySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# to return one subsidiaries.
class SubsidiariesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubsidiarySerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        return subsidiary

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({'detail': 'Subsidiary not found.'}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


# to retuen all Orgaization, with subsidiary With Budgets 
class OrganizationListView(ListAPIView):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        slug = self.request.query_params.get('slug', None)
        if slug:
            organizations = Organizations.objects.filter(slug=slug).all()
            for organization in organizations:
                organization.subsidiaries = Subsidiaries.objects.filter(organization=organization)
                for subsidiary in organization.subsidiaries:
                    subsidiary.budgets = Budgets.objects.filter(subsidiary=subsidiary)
            return organizations
        else:
            return Organizations.objects.none()


class SubsidiariesProjectsListView(generics.ListAPIView):
    serializer_class = SubsidiariesSerializer

    def get_queryset(self):
        slug = self.request.query_params.get('slug', None)
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        return [subsidiary]
class SubsidiariesProjectsListView(generics.ListAPIView):
    serializer_class = ProjectsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        slug = self.request.query_params.get('slug', None)
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        projects = Projects.objects.filter(subsidiary=subsidiary)
        
        return projects
    
class SubsidiariesDetailsView(generics.RetrieveAPIView):
    serializer_class = SubsidiariesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        slug = self.request.query_params.get('slug', None)
        subsidiary = get_object_or_404(Subsidiaries, slug=slug)
        return subsidiary

    def retrieve(self, request, *args, **kwargs):
        subsidiary = self.get_object()
        projects = Projects.objects.filter(subsidiary=subsidiary)
        projects_serializer = ProjectsSerializer(projects, many=True)
        budgets = Budgets.objects.filter(subsidiary=subsidiary)
        budgets_serializer = BudgetSerializer(budgets, many=True)
        response_data = {
            "subsidiary": SubsidiariesSerializer(subsidiary).data,
            "projects": projects_serializer.data,
            "budgets": budgets_serializer.data,
        }

        return Response(response_data)
    
class ProjectDetailsWithEmployeeAndClientView(generics.RetrieveAPIView):
    serializer_class = ProjectWithEmployeeAndClientSerializer
    queryset = Projects.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]


    def retrieve(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('project_id')
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
        
        
class InvoiceListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        # Get the invoice number from the query parameters
        invoice_number = self.request.query_params.get('invoice_number')

        try:
            # Retrieve the invoice by invoice_number
            invoice = Invoice.objects.get(invoice_number=invoice_number)
        except Invoice.DoesNotExist:
            return Response(
                {"detail": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the invoice, including related user and items
        serializer = InvoiceSerializer(invoice)

        return Response(serializer.data)
    
class InvoiceDetailView(APIView):
   def get(self, request, invoice_number, format=None):
        invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
        serializer = InvoiceGetSerializer(invoice)
        response_data = serializer.data
        return Response(response_data)
        response_data = {
            'user': user_data,
            'items': items_data,
            'address': address_data,
            'payments': payment_data
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
    
      
class PaymentHistoryAPIView(generics.ListCreateAPIView):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class ClientRegistration(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
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
    
    def post(self, request, format=None):
        request_data = request.data.copy()
        request_data['user']['is_client'] = True
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

        # Create a new user if it doesn't exist
        if create or user_instance is None:
            user_serializer = UserRegSerializer(data=request.data.get('user', {}))
        else:
            # Update user data, keeping existing data for fields not provided in the request
            user_serializer = UserRegSerializer(user_instance, data=request.data.get('user', {}), partial=True)

        if user_serializer.is_valid():
            user_instance = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Client data if it exists
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
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if create:
            return Response({"message": "Client registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Client information updated successfully"}, status=status.HTTP_200_OK)
    
            
class EmployeeRegistration(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
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

        user_serializer = UserRegSerializer(user_instance)

        response_data = {
            "user": user_serializer.data,
            "employee": employee_serializer.data if employee_serializer else None,
            "address": address_serializer.data if address_serializer else None
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        request_data = request.data.copy()
        request_data['user']['is_employee'] = True
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

        # Create a new user if it doesn't exist
        if create or user_instance is None:
            user_serializer = UserRegSerializer(data=request.data.get('user', {}))
        else:
            # Update user data, keeping existing data for fields not provided in the request
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
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if create:
            return Response({"message": "Employee registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Employee information updated successfully"}, status=status.HTTP_200_OK)
    
  