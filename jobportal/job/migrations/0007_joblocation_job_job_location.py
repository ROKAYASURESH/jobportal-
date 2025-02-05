# Generated by Django 5.0.7 on 2024-07-21 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_rename_job_type_job_type_job_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='job_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.joblocation'),
        ),
    ]
