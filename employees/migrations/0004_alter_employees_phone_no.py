# Generated by Django 4.2.4 on 2023-09-02 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_employees_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='phone_no',
            field=models.IntegerField(),
        ),
    ]
