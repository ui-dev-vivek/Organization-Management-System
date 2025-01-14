# Generated by Django 4.2.4 on 2023-09-09 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=255)),
                ('apt_suite_number', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=10)),
                ('country', models.CharField(default='United States', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('invoice_number', models.CharField(max_length=20, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('due_date', models.DateField()),
                ('payment_method', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(max_length=100)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_invoices', to='payments.address')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_invoices', to='payments.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, null=True)),
                ('payment_status', models.CharField(choices=[('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')], max_length=20)),
                ('invoice', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='payments.invoice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_histories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='payments.invoice')),
            ],
        ),
    ]
