from django.contrib import admin
from .models import Employees
from authapp.models import User, Address
from .forms import EmployeeForm

class AddressAdmin(admin.StackedInline):
    model = Address
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    exclude = ('user',)
    list_display = (
        "get_user_name",
        "get_user_full_name",
        "get_organization_name",
        "get_subsidiary_name",
        'emp_type',
        "phone_no",
    )
    def get_organization_name(self, obj):
        return obj.subsidiary.organization.name

    get_organization_name.short_description = "Organization Name"

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = "User Id"

    def get_user_full_name(self, obj):
        return obj.user.first_name +" "+ obj.user.last_name
    
    get_user_full_name.short_description = "Client Name"

    def get_subsidiary_name(self, obj):
        return obj.subsidiary.name

    get_subsidiary_name.short_description = "Subsidiary Name"
    # inlines=['AddressAdmin']
    fieldsets = (
        ('User Information', {
            'fields': ('subsidiary','username', 'password','confirm_password', 'email', 'first_name','last_name')
        }),
        ('Address:', {
            'fields': ('street_address', 'apt_suite_number','city', 'state', 'zip_code', 'country')
        }),
        ('Uploader Profile Information', {
            'fields': ('phone_no', 'emp_type', 'profile_image')
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj:  # Editing an existing client
            initial_data = {
                'username': obj.user.username,
                'email': obj.user.email,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'password': "",  # Leave password field empty for editing
                'confirm_password': "",  # Also leave confirm_password empty
                'phone_no': obj.phone_no,
                'emp_type': obj.emp_type,
                'profile_image': obj.profile_image,
            }
            
            address = obj.user.address

            if address:
                initial_data.update({
                    'street_address': address.street_address,
                    'apt_suite_number': address.apt_suite_number,
                    'city': address.city,
                    'state': address.state,
                    'zip_code': address.zip_code,
                    'country': address.country,
                })
                form.base_fields['confirm_password'].required = False  # Allow empty confirm_password field

                for field_name, value in initial_data.items():
                    if field_name in form.base_fields:
                        form.base_fields[field_name].initial = value

        return form

    def save_model(self, request, obj, form, change):
        user = User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            is_employee=True,
            is_client=False
        )
        user.set_password(form.cleaned_data['password'])
        user.save()

        address = Address(
            street_address=form.cleaned_data['street_address'],
            apt_suite_number=form.cleaned_data['apt_suite_number'],
            city=form.cleaned_data['city'],
            zip_code=form.cleaned_data['zip_code'],
            state=form.cleaned_data['state'],
            country=form.cleaned_data['country'],
            user=user  # Associate the address with the user
        )
        address.save()  # Address will be saved with the correct user association

        obj.user = user
        obj.save()

    

admin.site.register(Employees,EmployeeAdmin)

