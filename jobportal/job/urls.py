from django.urls import path
from .views import *
urlpatterns = [
    path('', HOME, name='home'),
    path('job/', JOB, name='job'),
    path('about/', ABOUT, name='about'),
    path('job_details/', JOB_DETAILS, name='job_details'),
    path('contact/', CONTACT, name='contact'),
    # USER AUTHENTICAION
    path('user_signup/',  SIGN_UP, name='user_signup'),
    path('user_login/',  USER_LOGIN, name='user_login'),
    path('logout/',  USER_LOGOUT, name='logout'),
]
