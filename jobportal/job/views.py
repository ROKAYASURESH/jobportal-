from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.
def JOB_USER(request):
    return render(request, 'base/common.html')

def HOME(request):
    return render(request, 'main/home.html')

def JOB(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'main/job.html')

def ABOUT(request):
    return render(request, 'main/about.html')

def CONTACT(request):
    return render(request, 'main/contact.html')

def JOB_DETAILS(request):
    return render(request, 'main/job_details.html')

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
    return render(request, "admin_dashboard/main.html")
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

