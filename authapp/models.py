from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.username + " : "+self.email

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street_address = models.CharField(max_length=255,null=True)
    apt_suite_number = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="United States")

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.state} {self.zip_code}'
    
class ApiAdminAction(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE ,related_name='api_admin_action')
    action=models.BooleanField();
    def __str__(self):
        return f"{self.user.username}"
    