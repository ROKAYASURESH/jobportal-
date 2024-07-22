from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Job_type)
admin.site.register(Experience)
admin.site.register(Apply)
admin.site.register(JobLocation)