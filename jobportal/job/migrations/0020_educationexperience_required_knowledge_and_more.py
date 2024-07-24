# Generated by Django 5.0.7 on 2024-07-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0019_employers_company_des'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Required_Knowledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirement', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='job',
            old_name='employers',
            new_name='recruiter',
        ),
        migrations.RemoveField(
            model_name='job',
            name='experience',
        ),
        migrations.AddField(
            model_name='job',
            name='experience',
            field=models.ManyToManyField(to='job.experience'),
        ),
    ]
