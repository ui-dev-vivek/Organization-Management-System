from rest_framework import serializers
from authapp.models import User,Address
from employees.models import Employees
from subsidiaries.models import Organizations,Subsidiaries,Budgets
from employees.models import Employees
from clients.models import Clients
from projects.models import Projects,EmployeeOnProject,ClientOnProject
from payments.models import Invoice, Item,PaymentHistory

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budgets
        fields = '__all__'



class SubsidiarySerializer(serializers.ModelSerializer):
    budgets = BudgetSerializer(many=True, read_only=True)

    class Meta:
        model = Subsidiaries
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    subsidiaries = SubsidiarySerializer(many=True, read_only=True)

    class Meta:
        model = Organizations
        fields = '__all__'
    
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

class SubsidiariesSerializer(serializers.ModelSerializer):
    projects = ProjectsSerializer(many=True, read_only=True)

    class Meta:
        model = Subsidiaries
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employees
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Clients
        fields = '__all__'

class ProjectWithEmployeeAndClientSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True, source='employeeonproject_set.employees')
    clients = ClientSerializer(many=True, read_only=True, source='clientonproject_set.clients')

    class Meta:
        model = Projects
        fields = '__all__'
        
        


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer(source='user.address', read_only=True)
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'



    
class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'