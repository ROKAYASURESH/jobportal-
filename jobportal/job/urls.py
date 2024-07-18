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
    # RECRUITER AUTHENTICATION
    path('recruiter_signup/',  RECRUITER_SIGNUP, name='recruiter_signup'),
    path('recruiter_login/',  RECRUITER_LOGIN, name='recruiter_login'),
    # ADMIN
    path('admin_login/',  ADMIN_LOGIN, name='admin_login'),
    path('views_user/',  VIEWS_USERS, name='views_user'),
]
