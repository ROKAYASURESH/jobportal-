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
    
class Job_type(models.Model):
    job_type = models.CharField(max_length=200)

    def __str__(self):
        return self.job_type

class JobLocation(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name
class Experience(models.Model):
    label = models.CharField(max_length=50)  # e.g., "1-2 Years", "2-3 Years"

    def __str__(self):
        return self.label
    
class Job(models.Model):
    recruiter=models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    title=models.CharField(max_length=200, )
    salary=models.CharField(max_length=30)
    image=models.ImageField(upload_to='job')
    des=models.CharField(max_length=400)
    experience = models.ManyToManyField(Experience)
    location=models.CharField(max_length=150)
    job_location=models.ForeignKey(JobLocation, on_delete=models.CASCADE, null=True)
    skills=models.CharField(max_length=200, )
    creationdate=models.DateField(auto_now_add=True)
    job_type=models.ForeignKey(Job_type, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title
    
class Apply(models.Model):
    job=models.ForeignKey(Job, on_delete=models.CASCADE)
    student=models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    cv=models.FileField(null=True)
    applydate=models.DateField()


    def __str__(self):
        return f"Application by {self.student} for {self.job}" 
