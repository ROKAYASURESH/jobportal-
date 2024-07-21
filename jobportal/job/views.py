from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date
from .models import *
from datetime import datetime
# Create your views here.
def JOB_USER(request):
    return render(request, 'base/common.html')

def HOME(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    user = request.user
    job = Job.objects.all()
    list = []

    try:
        student = StudentUser.objects.get(user=user)
        data = Apply.objects.filter(student=student)
        for i in data:
            list.append(i.job.id)
    except StudentUser.DoesNotExist:
        student = None
        list = []

    context = {
        'job': job,
        'list': list,
    }
    return render(request, 'main/home.html', context)

def JOB(request):
    # if not request.user.is_authenticated:
    #     return redirect('user_login')
    user = request.user
    job_type = Job_type.objects.all()
    label = Experience.objects.all()
    jobs = Job.objects.all()
    job =Job.objects.all().count()

    list = []

    try:
        student = StudentUser.objects.get(user=user)
        data = Apply.objects.filter(student=student)
        for i in data:
            list.append(i.job.id)
    except StudentUser.DoesNotExist:
        student = None
        list = []
    context={
        'job_type':job_type,
        'jobs':jobs,
        'job':job,
        'label':label,
        'list':list
    }
    return render(request, 'main/job.html', context)

def filter_data(request):
    job_type=request.GET.getlist('job_type[]')
    experience_ids = request.GET.getlist('experience[]')

    if job_type:
        job=Job.objects.filter(job_type__id__in =job_type).order_by('-id')
    elif experience_ids:
        job = Job.objects.filter(experience__id__in=experience_ids)
    else:
        job= Job.objects.all().order_by('-id')

    t = render_to_string('ajax/job.html', {'job':job})
    return JsonResponse({'data': t})

def ABOUT(request):
    return render(request, 'main/about.html')

def CONTACT(request):
    return render(request, 'main/contact.html')

def JOB_DETAILS(request, id):
    job=Job.objects.get(id=id)
    context={
        'job':job
    }
    return render(request, 'main/job_details.html', context)

'''=================================================================
                    USER_AUTHENTICATION START
   =================================================================
'''
# User_Register
def SIGN_UP(request):
    error = " "
    if request.method == "POST" and request.FILES:
        firstname=request.POST['first_name']
        lastname=request.POST['last_name']
        image=request.FILES['image']
        password=request.POST['password']
        # confirm_password=request.POST['confirm_password']
        email=request.POST['email']
        contact=request.POST['contact']
        gender=request.POST['gender']

        try:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            StudentUser.objects.create(user=user, mobile=contact, image=image, gender=gender, type='student')
            error='No'
        except:
            error="yes"

    context={
        'error':error
    }      
    return render(request, 'auth/user_auth/user_signup.html', context)

# User_Login
def USER_LOGIN(request):
    error = " "
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == 'student':
                    login(request, user)
                    error='no'
                else:
                    error = 'yes'
            except:
                error = 'yes'
        else:
            error = 'yes'

    context={
        'error':error
    }
    return render(request, 'auth/user_auth/user_login.html', context)

# Logout
def USER_LOGOUT(request):
    logout(request)
    return redirect('user_login')
# ==================END========================

'''=================================================================
                    RECURATOR START
   =================================================================
'''
# Recurator_register
def RECRUITER_SIGNUP(request):
    error = " "
    if request.method == "POST" and request.FILES:
        firstname=request.POST['first_name']
        lastname=request.POST['last_name']
        image=request.FILES['image']
        password=request.POST['password']
        # confirm_password=request.POST['confirm_password']
        email=request.POST['email']
        contact=request.POST['contact']
        gender=request.POST['gender']
        company=request.POST['company']

        try:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            Recruiter.objects.create(user=user, mobile=contact, image=image, gender=gender, company=company, type='recruiter', status='pending')
            error='No'
        except:
            error="yes"

    context={
        'error':error
    }    
    return render(request, 'auth/recruiter/recruiter_signup.html', context)

# Recrutier_login
def RECRUITER_LOGIN(request):
    error = " "
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == 'recruiter' and user1.status!='pending':
                    login(request, user)
                    error='no'
                else:
                    error = 'not'
            except:
                error = 'yes'
        else:
            error = 'yes'

    context={
        'error':error
    }
    return render(request, 'auth/recruiter/recruiter_login.html', context)

'''=================================================================
                    ADMIN
   =================================================================
'''
# ADMIN_DASHBOARD:
def ADMIN_DASHBOARD(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    employer=Recruiter.objects.all().count()
    Jobseeker=StudentUser.objects.all().count()
    pending =Recruiter.objects.filter(status='pending').count()
    applied=Apply.objects.all().count()

    context={
        "employer":employer,
        "Jobseeker":Jobseeker,
        "pending":pending,
        'applied':applied
    }
    return render(request, "admin_dashboard/main.html", context)
# Admin_Login
def ADMIN_LOGIN(request):
    error = ''
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        
        try:
            if user.is_staff:
                login(request, user)
                error='no'
            else:
                error='yes'
        except:
            error='yes'
    context={
        'error':error
    }
    return render(request, 'auth/admin_auth/admin_login.html', context)

# Logout
def ADMIN_LOGOUT(request):
    logout(request)
    return redirect('admin_login')

# User Data
def VIEWS_USERS(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    context={
        'data':data
    }
    return render(request, "main/admin/views_user.html", context)

# user_Delete
def DELETE_USER(request, id):
    data =User.objects.get(id=id)
    data.delete()
    return redirect('views_user')

# Recuiter Pending Data Show
def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Recruiter.objects.filter(status='pending')
    context={
        'data':data
    }
    return render(request, "main/admin/recruiter_pending.html", context)

# Change_Status
def CHANGE_STATUS(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    error=''
    recruiter =Recruiter.objects.get(id=id)
    if request.method == "POST":
        status=request.POST['status']
        recruiter.status = status
        try:
            recruiter.save()
            error='no'
        except:
            error='yes'
    context={
        'recruiter':recruiter,
        'error':error
    }
    return render(request, "main/admin/change_status.html", context)


# Employer Accepted Data Show
def emplpyer_accept(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Recruiter.objects.filter(status='Accept')
    context={
        'data':data
    }
    return render(request, "main/admin/employer_accept.html", context)

# Employer Reject Data Show
def employer_reject(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Recruiter.objects.filter(status='Reject')
    context={
        'data':data
    }
    return render(request, "main/admin/employer_reject.html", context)

# Employer employer_all Data Show
def employer_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Recruiter.objects.all()
    context={
        'data':data
    }
    return render(request, "main/admin/employer_all.html", context)


def DELETE_EMPLOYER(request, id):
    data =User.objects.get(id=id)
    data.delete()
    return redirect('employer_all')

from django.contrib.auth.forms import PasswordChangeForm

def password_change(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user_form=PasswordChangeForm(user=request.user)
    if request.method =='POST':
        user_form=PasswordChangeForm(user=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_login')
    context={
        "user_form":user_form
    }
    return render(request, "main/change_password.html", context)


# EMPLOYER
def ADD_JOB(request):
    if request.method =="POST":
        job_title= request.POST['job_title']
        start_date= request.POST['start_date']
        end_date= request.POST['end_date']
        salary= request.POST['salary']
        image=request.FILES ['image']
        des= request.POST['desc']
        experience= request.POST['experience']
        location= request.POST['location']
        skills= request.POST['skill']
        employer=Recruiter.objects.get(user=request.user)
        try:
            Job.objects.create(recruiter=employer, title=job_title, start_date=start_date, end_date=end_date, salary=salary, image=image, des=des, 
                           experience=experience, location=location, skills=skills )
            messages.success(request, 'Job Detail has been added')
            return redirect('home')
        except ObjectDoesNotExist:
            messages.error(request, "Recruiter matching query does not exist.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
    return render(request, "main/employer/emp_job.html")


def job_list(request):
    employer = Recruiter.objects.get(user=request.user)
    job = Job.objects.filter(recruiter=employer)
    context={
        'job':job
    }
    return render(request, "main/employer/job_list.html" ,context)


def edit_jobdetails(request, id):
    job = Job.objects.get(id=id)
    if request.method =="POST":
        job.title= request.POST['job_title']
        start_date= request.POST['start_date']
        end_date= request.POST['end_date']
        job.salary= request.POST['salary']
        image= request.POST['image']
        
        job.des= request.POST['desc']
        job.experience= request.POST['experience']
        job.location= request.POST['location']
        job.skills= request.POST['skill']
        
        try:
            job.save()
            messages.success(request, 'Job Detail has been updated')
            return redirect('home')
        except ObjectDoesNotExist:
            messages.error(request, "Recruiter matching query does not exist.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        
        if start_date:
            job.start_date=start_date
            job.save()
        else:
            pass
        if end_date:
            job.end_date=end_date
            job.save()

        else:
            pass
        if image:
            job.image=image
            job.save()

        else:
            pass
    context={
        'job':job,
    }
    return render(request, "main/employer/edit_jobDetail.html", context)



from django.utils import timezone
# APPLY for a job
def apply(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user
    today_date = timezone.now().date()

    # Check if the student profile exists
    student = StudentUser.objects.filter(user=user).first()
    if not student:
        messages.error(request, 'Student profile not found.')
        return redirect('home')  # Redirect to an error page or some appropriate URL

    # Check if the job exists
    job = Job.objects.filter(id=id).first()  # Changed to Job from StudentUser
    if not job:
        messages.error(request, 'Job not found.')
        return redirect('home')  # Redirect to an error page or some appropriate URL

    if job.end_date < today_date:
        messages.error(request, 'Date expired')
    elif job.start_date > today_date:
        messages.error(request, 'Job not open yet')
    else:
        if request.method == "POST":
            cv = request.FILES.get('cv')
            if cv:
                Apply.objects.create(student=student, job=job, cv=cv, applydate=today_date)
                messages.success(request, 'Application submitted successfully.')
                return redirect("home")
            else:
                messages.error(request, 'CV file is missing.')

    return render(request, "main/apply.html")


def candidatelist(request):
    data = Apply.objects.all()
    context={
        "data":data
    }
    return render(request, 'main/employer/candidatelist.html', context)

def all_applied_list(request):
    all = Apply.objects.all()
    context={
        "all":all
    }
    return render(request, 'main/admin/all_applied_list.html', context)