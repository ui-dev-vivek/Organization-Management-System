# Generated by Django 4.2.4 on 2023-10-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_remove_invoice_billing_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='transaction_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
