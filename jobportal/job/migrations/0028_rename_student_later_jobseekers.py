# Generated by Django 5.0.7 on 2024-07-25 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0027_later'),
    ]

    operations = [
        migrations.RenameField(
            model_name='later',
            old_name='student',
            new_name='jobseekers',
        ),
    ]
