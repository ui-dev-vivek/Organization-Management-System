from django.contrib import admin
# from employees.models import Employees
from authapp.models import User, Address

# from django import forms


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance.pk:
#             if self.instance.is_client:
#                 self.fields['organization_name'] = forms.CharField()
#                 self.fields['phone_no'] = forms.IntegerField()
#                 # Aur jo bhi fields Clients me hain, woh yaha add karo
                
#             elif self.instance.is_employee:
#                 self.fields['emp_type'] = forms.ChoiceField(choices=Employees.EMP_TYPE_CHOICES)
#                 self.fields['phone_no'] = forms.IntegerField()
#                 # Aur jo bhi fields Employees me hain, woh yaha add karo

# class UserAdmin(admin.ModelAdmin):
#     form = UserForm

admin.site.register(User)
admin.site.register(Address)
# admin.site.register(Employees)
