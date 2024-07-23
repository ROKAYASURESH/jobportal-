# Generated by Django 5.0.7 on 2024-07-22 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0012_rename_recruiter_employers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employers',
            name='type',
        ),
        migrations.RemoveField(
            model_name='jobseekers',
            name='type',
        ),
        migrations.AddField(
            model_name='employers',
            name='is_employer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobseekers',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]
