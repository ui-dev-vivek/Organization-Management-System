# Generated by Django 4.2.4 on 2023-09-07 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subsidiaries', '0003_budgets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgets',
            name='subsidiary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsidiary', to='subsidiaries.subsidiaries'),
        ),
        migrations.AlterField(
            model_name='subsidiaries',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='subsidiaries.organizations'),
        ),
    ]