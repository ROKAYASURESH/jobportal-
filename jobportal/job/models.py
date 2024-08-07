from django.db import models
from datetime import date
from django.contrib.auth.models import User

#! JOBSEEKERS: =================================
# models.py
from django.db import models
from django.contrib.auth.models import User
import datetime
import random

class JobSeekers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.ImageField(null=True, upload_to='user_profile')
    gender = models.CharField(max_length=10, null=True)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        diff = now - self.created_at
        return diff.total_seconds() < 300  # 5 minutes validity

#! EMPLOYERS: ==================================================   
class Employers(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    company=models.CharField(max_length=200, null=True)
    company_des=models.CharField(max_length=400, null=True)
    mobile=models.CharField(max_length=15, null= True)
    image=models.ImageField(null=True, upload_to='user_profile')
    web=models.CharField(max_length=100, null=True)
    is_employer = models.BooleanField(default=False)
    status=models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return self.user.username

#! JOB_TYPES: =====================================
class Job_type(models.Model):
    job_type = models.CharField(max_length=200)

    def __str__(self):
        return self.job_type

#! JOB_EXPERIENCE: ====================================
class Experience(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label

# ! notification  starr
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

#! end
#! JOB DETAILS: ============================================   

class Job(models.Model):
    employers = models.ForeignKey('Employers', on_delete=models.CASCADE)
    vacency = models.IntegerField(null=True)
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.CharField(max_length=30)
    image = models.ImageField(upload_to='job')
    des = models.CharField(max_length=400)
    location = models.CharField(max_length=150)
    skills = models.CharField(max_length=200)
    creationdate = models.DateField(auto_now_add=True)
    job_type = models.ForeignKey('Job_type', on_delete=models.CASCADE, null=True)
    experiences = models.ForeignKey('Experience', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title
    
    def remaining_days(self):
        return (self.end_date - date.today()).days
    
class Required_Knowledge(models.Model):
    job=models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    requirement = models.CharField(max_length=200)
    requirement2 = models.CharField(max_length=200, null=True)
    requirement3 = models.CharField(max_length=200, null=True)
    requirement4 = models.CharField(max_length=200, null=True)
    requirement5 = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.requirement
    
class EducationExperience(models.Model):
    job=models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    education = models.CharField(max_length=200)
    education1 = models.CharField(max_length=200, null=True)
    education2 = models.CharField(max_length=200, null=True)
    education3 = models.CharField(max_length=200, null=True)
    education4 = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.education

#! start
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
@receiver(post_save, sender=Job)
def send_job_notification(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"A new job '{instance.title}'has been posted by ({ instance.employers.company} ) Company"
            )
# ! End
    
#! JOBSEEKER APPLY FOR JOB: =========================  
class Apply(models.Model):
    job=models.ForeignKey(Job, on_delete=models.CASCADE)
    student=models.ForeignKey(JobSeekers, on_delete=models.CASCADE)
    cv=models.FileField(null=True)
    applydate=models.DateField()

    def __str__(self):
        return f"Application by {self.student} for {self.job}" 

#! ADMINPROFILE: =================================================   
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True, null=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username
    

    # LATER
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_jobs = models.ManyToManyField(Job, related_name='saved_by')

    def __str__(self):
        return self.user.username
    