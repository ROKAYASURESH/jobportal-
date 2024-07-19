from django.urls import path
from .views import *
urlpatterns = [
    path('job_user/', JOB_USER, name='job_user'),
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
    # ADMIN============
   
    path('admin_dashboard/',  ADMIN_DASHBOARD, name='admin_dashboard'),
    path('admin_login/',  ADMIN_LOGIN, name='admin_login'),
     # ------------user-------------
    path('views_user/',  VIEWS_USERS, name='views_user'),
   
    path('delete_user/<int:id>',  DELETE_USER, name='delete_user'),
    path('recruiter_pending',  recruiter_pending, name='recruiter_pending'),
    path('change_status/<int:id>',  CHANGE_STATUS, name='change_status'),
    path('emplpyer_accept',  emplpyer_accept, name='emplpyer_accept'),
    path('employer_reject',  employer_reject, name='employer_reject'),
    path('employer_all',  employer_all, name='employer_all'),
    path('delete_employer<int:id>',  DELETE_EMPLOYER, name='delete_employer'),
    
    

]
