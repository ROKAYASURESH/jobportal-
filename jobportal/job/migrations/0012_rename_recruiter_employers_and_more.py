# Generated by Django 5.0.7 on 2024-07-22 15:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_rename_studentuser_jobseekers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recruiter',
            new_name='Employers',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='recruiter',
            new_name='employers',
        ),
    ]
