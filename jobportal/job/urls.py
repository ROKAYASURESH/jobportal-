from django.urls import path
from job.views import (
    JOB_USER, HOME, JOB, ABOUT, CONTACT, JOB_DETAILS, apply, 
    SIGN_UP, USER_LOGIN, USER_LOGOUT, user_profile, password_change,
    filter_data, all_applied_list, filter_jobs_by_end_date, 
    ADD_JOB, job_list, candidatelist, edit_jobdetails, 
    emp_dash, EMPLOYER_SIGNUP, EMPLOYER_LOGIN, Employer_LOGOUT, 
    emp_profile, emp_password_change, ADMIN_DASHBOARD, ADMIN_LOGIN, 
    ADMIN_LOGOUT, admin_profile, admin_password_change, VIEWS_USERS, 
    DELETE_USER, recruiter_pending, CHANGE_STATUS, emplpyer_accept, 
    employer_reject, employer_all, DELETE_EMPLOYER
)
from .views import filter_jobs_by_end_date
from job.views import *
urlpatterns = [
    #! FOR JOBSEEKER SIDE
    path('job_user/', JOB_USER, name='job_user'),
    path('', HOME, name='home'),
    path('job/', JOB, name='job'),
    path('about/', ABOUT, name='about'),
    path('contact/', CONTACT, name='contact'),
    path('job_details/<int:id>', JOB_DETAILS, name='job_details'),
    path('applyforjob/<int:id>',  apply, name='applyforjob'),
    # JOBSEEKER AUTHENTICAION
    path('user_signup/',  SIGN_UP, name='user_signup'),
    path('user_login/',  USER_LOGIN, name='user_login'),
    path('logout/',  USER_LOGOUT, name='logout'),
     path('user/profile/', user_profile, name='user_profile'),
    path('password_change/' , password_change, name="password_change"),

    # AJAX
    path('product/filter-data',filter_data,name="filter-data"),
    path('all_applied_list',  all_applied_list, name='all_applied_list'),
    path('filter_jobs_by_end_date/', filter_jobs_by_end_date, name='filter_jobs_by_end_date'),


    #! FOR EMPLOYER
    path('add_job/' , ADD_JOB, name="add_job"),
    path('job_list/' , job_list, name="job_list"),
    path('candidatelist',  candidatelist, name='candidatelist'),
    path('edit_jobdetails/<int:id>',  edit_jobdetails, name='edit_jobdetails'),
    path('edit_jobdetails/<int:id>',  edit_jobdetails, name='edit_jobdetails'),
    # employer Authentication
    path('emp_dash/',  emp_dash, name='emp_dash'),
    path('employer_signup/',  EMPLOYER_SIGNUP, name='employer_signup'),
    path('employer_login/',  EMPLOYER_LOGIN, name='employer_login'),
    path('emp_logout/',  Employer_LOGOUT, name='emp_logout'),
    path('emp_profile',  emp_profile, name='emp_profile'),
    path('emp_password_change',  emp_password_change, name='emp_password_change'),

    # ADMIN============
   
    path('admin_dashboard/',  ADMIN_DASHBOARD, name='admin_dashboard'),
    path('admin_login/',  ADMIN_LOGIN, name='admin_login'),
    path('admin_logout/',  ADMIN_LOGOUT, name='admin_logout'),
    path('admin_profile/',  admin_profile, name='admin_profile'),
    path('admin_password_change/',  admin_password_change, name='admin_password_change'),
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


