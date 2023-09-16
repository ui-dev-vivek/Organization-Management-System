from django.db import models
# from django.contrib.auth.models import User
from authapp.models import User
from Base.models import BaseModel
from subsidiaries.models import Subsidiaries
from django.core.validators import FileExtensionValidator


def validate_image_aspect_ratio(image):
    width, height = image.size
    if width != height:
        raise ValidationError("Only 1:1 aspect ratio images are allowed.")


class Employees(BaseModel):
    EMP_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('freelancer', 'Freelancer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subsidiary = models.ForeignKey(Subsidiaries, on_delete=models.CASCADE)
    phone_no = models.IntegerField(unique=False)
    emp_type = models.CharField(max_length=20, choices=EMP_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to='static/profile_images/', null=True,
                                      validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            
        ])
    
    def __str__(self):
        return self.user.username
   
    USERNAME_FIELD = 'username'
    