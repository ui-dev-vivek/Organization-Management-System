from django.db import models
# from django.contrib.auth.models import User
from authentication.models import User
from Base.models import BaseModel
from subsidiaries.models import Subsidiaries

class Employees(BaseModel):
    EMP_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('freelancer', 'Freelancer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subsidiary = models.ForeignKey(Subsidiaries, on_delete=models.CASCADE)
    phone_no = models.IntegerField(unique=True)
    emp_type = models.CharField(max_length=20, choices=EMP_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', null=True)