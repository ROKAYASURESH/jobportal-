from django.urls import path
from .views import *
urlpatterns = [
    path('', HOME, name='home'),
    path('job/', JOB, name='job'),
    path('about/', ABOUT, name='about'),
    path('job_details/', JOB_DETAILS, name='job_details'),
    path('contact/', CONTACT, name='contact'),
]
