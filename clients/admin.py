from django.contrib import admin
from .models import Clients
from authapp.models import User, Address
from .forms import ClientForm
from django.db import IntegrityError
class AddressAdmin(admin.StackedInline):
    model = Address
    extra = 1

class ClientsAdmin(admin.ModelAdmin):
    form = ClientForm
    exclude = ('user',)
    list_display = (
        "get_user_name",
        "get_user_full_name",
        "get_organization_name",
        "get_subsidiary_name",
        'organization_name',
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
    fieldsets = (
        ('User Information', {
            'fields': ('subsidiary','username', 'password','confirm_password', 'email', 'first_name','last_name')
        }),
        ('Address:', {
            'fields': ('street_address', 'apt_suite_number','city', 'state', 'zip_code', 'country')
        }),
        ('Uploader Profile Information', {
            'fields': ('phone_no', 'organization_name', 'profile_image')
        }),
    )
    search_fields = ['subsidiary__name','user__username','user__email'] 
    ordering = ['user__username']  
    list_filter = ('subsidiary',) 
    autocomplete_fields = ['subsidiary']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Reset initial values every time form is fetched
        for field_name in form.base_fields:
            form.base_fields[field_name].initial = None

        if obj:  # Editing an existing client
            user = obj.user
            form.base_fields['username'].initial = user.username
            form.base_fields['email'].initial = user.email
            form.base_fields['first_name'].initial = user.first_name
            form.base_fields['last_name'].initial = user.last_name
            
            try:
                address = user.address
                form.base_fields['street_address'].initial = address.street_address
                form.base_fields['apt_suite_number'].initial = address.apt_suite_number
                form.base_fields['city'].initial = address.city
                form.base_fields['state'].initial = address.state
                form.base_fields['zip_code'].initial = address.zip_code
                form.base_fields['country'].initial = address.country
            except Address.DoesNotExist:
                pass
                
        return form

    def save_model(self, request, obj, form, change):
        try:
            if change:  # Updating an existing client
                user = obj.user
            else:
                user = User()

            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_employee = False
            user.is_client = True
            
            if form.cleaned_data['password']:  # check if a new password is provided
                user.set_password(form.cleaned_data['password'])
            
            user.save()

            address, created = Address.objects.get_or_create(user=user)
            address.street_address = form.cleaned_data['street_address']
            address.apt_suite_number = form.cleaned_data['apt_suite_number']
            address.city = form.cleaned_data['city']
            address.zip_code = form.cleaned_data['zip_code']
            address.state = form.cleaned_data['state']
            address.country = form.cleaned_data['country']
            address.save()

            obj.user = user
            obj.save()

        except IntegrityError:
            # Capture the unique constraint violation for the username
            msg = "A user with this username already exists."
            self.message_user(request, msg,)
            return
admin.site.register(Clients, ClientsAdmin)

#code Closed!