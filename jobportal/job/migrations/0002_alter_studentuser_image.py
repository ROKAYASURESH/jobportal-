# Generated by Django 5.0.7 on 2024-07-18 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentuser',
            name='image',
            field=models.ImageField(null=True, upload_to='user_profile'),
        ),
    ]
