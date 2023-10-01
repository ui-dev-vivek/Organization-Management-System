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
        
class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
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




    
class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'
   
   
class ClientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

class EmployeeRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'
        

# class AddressSerializer(serializers.ModelSerializer):
#     address = UserSerializer()
#     class Meta:
#         model = Address
#         fields = "__all__"

class InvoiceGetSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)  
    class Meta:
        model = Invoice
        fields = '__all__'
    

   

class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)  # Make items not required during update
    
    class Meta:
        model = Invoice
        fields = '__all__'

    

    def update(self, instance, validated_data):
        # Update invoice fields
        instance.user = validated_data.get('user', instance.user)
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.tax_rate = validated_data.get('tax_rate', instance.tax_rate)

        # Update items if provided in the payload
        items_data = validated_data.get('items')
        if items_data is not None:
            instance.items.all().delete()  # Clear existing items
            for item_data in items_data:
                Item.objects.create(invoice=instance, **item_data)

        instance.save()
        return instance