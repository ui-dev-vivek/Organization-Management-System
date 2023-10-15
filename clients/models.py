from django.db import models
from authapp.models import User
from subsidiaries.models import Subsidiaries
from django.core.validators import FileExtensionValidator
from Base.models import BaseModel

class Clients(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subsidiary = models.ForeignKey(Subsidiaries, on_delete=models.CASCADE)
    phone_no = models.IntegerField(unique=False)
    organization_name = models.CharField(max_length=255) 
    profile_image = models.ImageField(upload_to='profile_images/', null=True,default='static/profile_images/default.png',
                                      validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            
        ])
    def __str__(self):
        return self.user.first_name
   
#code Closed!