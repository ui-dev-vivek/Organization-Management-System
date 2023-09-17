from django.db import models
from authapp.models import User
from Base.models import BaseModel

import uuid;

class Invoice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)  # Make it non-editable
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    due_date = models.DateField()
    payment_method = models.CharField(max_length=50)      
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    

    def save(self, *args, **kwargs):        
        if not self.invoice_number:
            unique_id = uuid.uuid4().hex[:8]  # Generate a unique ID
            self.invoice_number = f"DYR-{unique_id}"

        super(Invoice, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'Invoice {self.invoice_number} - {self.user}'


class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    

class PaymentHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_histories')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments', default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')])

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.payment_date}'

#Code Closed