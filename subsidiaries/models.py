from django.db import models
from Base.models import BaseModel
from django.core.validators import FileExtensionValidator

class Organizations(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description=models.TextField()
    logo = models.ImageField(upload_to='static/logos/', null=True,
                                      validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            
        ])
    
    def __str__(self):
        return self.name

class Subsidiaries(BaseModel):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE,related_name='organization')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description=models.TextField()
    logo = models.ImageField(upload_to='static/logos/', null=True,
                                      validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            
        ])
    
    def __str__(self):
        return self.name 
    
class Budgets(BaseModel):
    subsidiary = models.ForeignKey(Subsidiaries, on_delete=models.CASCADE,related_name='subsidiary')
    year = models.IntegerField()
    amount = models.FloatField()
    def __str__(self):
        return 'Budgets of '+self.subsidiary.name
# Code Closed!