# Generated by Django 4.2.4 on 2023-09-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projecttask_taskchecklist_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttask',
            name='state',
            field=models.CharField(choices=[('todo', 'Todo'), ('dowing', 'Doing'), ('done', 'Done'), ('testing', 'Testing'), ('done', 'Done')], default='todo', max_length=20),
        ),
    ]