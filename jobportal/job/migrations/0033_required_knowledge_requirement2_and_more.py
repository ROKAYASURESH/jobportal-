# Generated by Django 5.0.7 on 2024-07-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0032_rename_experience_job_experiences'),
    ]

    operations = [
        migrations.AddField(
            model_name='required_knowledge',
            name='requirement2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='required_knowledge',
            name='requirement3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='required_knowledge',
            name='requirement4',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='required_knowledge',
            name='requirement5',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
