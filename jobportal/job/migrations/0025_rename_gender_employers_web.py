# Generated by Django 5.0.7 on 2024-07-25 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0024_remove_requirements_job_delete_educations_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employers',
            old_name='gender',
            new_name='web',
        ),
    ]