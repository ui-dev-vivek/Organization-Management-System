from rest_framework.generics import ListAPIView,RetrieveAPIView
# from rest_framework.generics import RetrieveAPIView
from rest_framework import generics,permissions
from employees.models import Employees
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from subsidiaries.models import Organizations,Subsidiaries,Budgets
from django.http import JsonResponse,Http404
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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