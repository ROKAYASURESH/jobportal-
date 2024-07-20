from django.db import models

from django.contrib.auth.models import User

class StudentUser(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15, null= True)
    image=models.ImageField(null=True, upload_to='user_profile')
    gender=models.CharField(max_length=10, null=True)
    type=models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return self.user.username
    
class Recruiter(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15, null= True)
    image=models.ImageField(null=True, upload_to='user_profile')
    gender=models.CharField(max_length=10, null=True)
    company=models.CharField(max_length=200, null=True)
    type=models.CharField(max_length=20, null=True)
    status=models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return self.user.username
    
class Job(models.Model):
    recruiter=models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    title=models.CharField(max_length=200, )
    salary=models.CharField(max_length=30)
    image=models.ImageField(upload_to='job')
    des=models.CharField(max_length=400)
    experience=models.CharField(max_length=100)
    location=models.CharField(max_length=150)
    skills=models.CharField(max_length=200, )
    creationdate=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title