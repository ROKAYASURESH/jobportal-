# Generated by Django 5.0.7 on 2024-07-21 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_apply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apply',
            old_name='jobseeker',
            new_name='student',
        ),
    ]
