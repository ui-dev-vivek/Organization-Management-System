# Generated by Django 4.2.4 on 2023-08-31 18:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subsidiaries', '0003_budgets'),
        ('clients', '0001_initial'),
        ('employees', '0003_alter_employees_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('project_desc', models.TextField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('start', 'Start'), ('working', 'Working'), ('complete', 'Complete'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], max_length=20)),
                ('subsidiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsidiaries.subsidiaries')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeOnProject',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_lead', models.BooleanField(default=False)),
                ('assigned_date', models.DateTimeField()),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employees')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projects')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientOnProject',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_date', models.DateTimeField()),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clients')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projects')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
