from django import forms

from authapp.models import  User, Address
from clients.models import Clients


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
    
    
    username = forms.CharField(label='Username',required=True)    
    email = forms.EmailField(label='Email',required=True)
    first_name = forms.CharField(label='First Name',required=True)
    last_name=forms.CharField(label='Last Name',required=True)    
    password = forms.CharField(widget=forms.PasswordInput(), label="Password",required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password",required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")

        if User.objects.filter(email=cleaned_data.get("email")).exists():
            raise forms.ValidationError("Email address already exists. Please use a different one.")

        return cleaned_data
    
    # AddressFormSet = forms.inlineformset_factory(User, Address, form=AddressForm, extra=1)
    
    street_address = forms.CharField(label='Street Address', max_length=255)
    apt_suite_number = forms.CharField(label='Apt/Suite Number', max_length=50, required=False)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=40)
    zip_code = forms.CharField(label='ZIP Code', max_length=10)
    country = forms.CharField(label='Country', max_length=100, initial="United States")
    
    
#code Closed!