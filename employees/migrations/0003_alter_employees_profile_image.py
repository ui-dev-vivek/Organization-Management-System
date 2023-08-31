# Generated by Django 4.2.4 on 2023-08-31 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employees_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='static/profile_images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]