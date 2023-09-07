from django.db import models
from Base.models import BaseModel
from subsidiaries.models import Subsidiaries
from employees.models import Employees
from clients.models import Clients
from django.utils.translation import gettext_lazy as _

class Projects(models.Model):
    PROJECT_STATUS = [
        ('start', _('Start')),
        ('working', _('Working')),
        ('complete', _('Complete')),
        ('pending', _('Pending')),
        ('cancelled', _('Cancelled')),
    ]

    subsidiary = models.ForeignKey(Subsidiaries, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    project_desc = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS)

    def __str__(self):
        return self.project_name

class EmployeeOnProject(BaseModel):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)    
    employees = models.ForeignKey(Employees, on_delete=models.CASCADE)
    is_lead=models.BooleanField(default=False)
    assigned_date = models.DateTimeField()
   
class ClientOnProject(BaseModel):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)    
    clients = models.ForeignKey(Clients, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField()

