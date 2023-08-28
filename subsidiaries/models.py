from django.db import models
from Base.models import BaseModel
# Create your models here.
class Organizations(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description=models.TextField()

class Subsidiaries(BaseModel):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description=models.TextField()