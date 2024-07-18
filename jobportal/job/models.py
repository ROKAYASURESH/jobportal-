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