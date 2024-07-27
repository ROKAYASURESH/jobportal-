from django.contrib import admin

# Register your models here.
from .models import *
class EducationExperience_TabularInLine(admin.TabularInline):
    model=EducationExperience
class Required_Knowledge_TabularInLine(admin.TabularInline):
    model=Required_Knowledge

class job_admin(admin.ModelAdmin):
    inlines =(EducationExperience_TabularInLine, Required_Knowledge_TabularInLine)

admin.site.register(Job, job_admin)
admin.site.register(JobSeekers)
admin.site.register(Employers)
admin.site.register(Job_type)
admin.site.register(Experience)
admin.site.register(Apply)
admin.site.register(UserProfile)