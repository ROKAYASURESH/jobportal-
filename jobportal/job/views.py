from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.
def HOME(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'main/home.html')
def JOB(request):
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

def USER_LOGOUT(request):
    logout(request)
    return redirect('user_login')
# ==================END========================

'''=================================================================
                    RECURATOR START
   =================================================================
'''

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

