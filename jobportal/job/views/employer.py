from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date
from job.models import *
from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from job.form import AdminProfileUpdateForm, AdminJobseekerUpdateForm, AdminEmployerUpdateForm

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

#! EMPLOYER _DASHBOARD
def emp_dash(request):
    user = request.user
    try:
        employer = Employers.objects.get(user=user)
    except Employers.DoesNotExist:
        employer = None
    context = {
        'employer': employer,
    }
    return render(request, "main/employer/base_home.html")

#! EMPLOYER SIGNUP: =============================================
def EMPLOYER_SIGNUP(request):
    if request.method == "POST" and request.FILES:
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        contact = request.POST['contact']
        gender = request.POST['gender']
        company = request.POST['company']

        try:
            # Validate the password
            validate_password(password)
            
            # Check if the passwords match
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'auth/employer/employer_signup.html', {
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                    'contact': contact,
                    'company': company,
                    'image': image
                })
            
            # Check if the email is already in use
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already exists!")
                return render(request, 'auth/employer/employer_signup.html', {
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                    'contact': contact,
                    'company': company,
                    'image': image
                })
            
            # Create the user and associated Employer profile
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            Employers.objects.create(user=user, mobile=contact, image=image, gender=gender, company=company, is_employer = True, status='pending')
            messages.success(request, f'Registration successful, {firstname}! Welcome JopPortal')
            return redirect('employer_login')
        
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'auth/employer/employer_signup.html', {
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'contact': contact,
                'company': company,
                'image': image
            })

    return render(request, 'auth/employer/employer_signup.html')

#! EMPLOYER LOGIN: ==================================================
def EMPLOYER_LOGIN(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user1 = Employers.objects.get(user=user)
                if user1.is_employer and user1.status!='pending':
                    login(request, user)
                    messages.success(request, f'You have successfully logged in {username}')
                    return redirect('emp_dash')
                else:
                   messages.error(request, "Your Status is currently pending !!")
            except:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/employer/employer_login.html')

#! EMPLOYER LOGOUT: ===================================================
def Employer_LOGOUT(request):
    logout(request)
    messages.success(request, 'You have successfully logged out,')
    return redirect('employer_login')

#! EMPLOYER PROFILE UPDATE: ================================================
def emp_profile(request):
    # Get or create the JobSeekers profile for the current user
    profile, created = Employers.objects.get_or_create(user=request.user)
    profile_form = AdminEmployerUpdateForm(instance=profile)

    if request.method == "POST":
        profile_form = AdminEmployerUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('emp_profile')

    context = {
        'profile_form': profile_form,
        'user': request.user,
        'profile': profile,  # Updated to directly pass the profile object
    }
    return render(request, "auth/employer/emp_profile.html", context)

#! EMPLOYER PASSWORD CHANGE: =====================================================
def emp_password_change(request):
    form = PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password change successfully')
            return redirect('employer_login')
        else:
            messages.error(request, 'something went wrong !!')

    context={
        'form':form,
    }
    return render(request, "auth/employer/emp_password_change.html", context)



#! EMPLOYER ADD_JOB FORM: ===================================================
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
        employer=Employers.objects.get(user=request.user)
        try:
            Job.objects.create(employers=employer, title=job_title, start_date=start_date, end_date=end_date, salary=salary, image=image, des=des, 
                           experience=experience, location=location, skills=skills )
            messages.success(request, 'Job Detail has been added')
            return redirect('emp_dash')
        except ObjectDoesNotExist:
            messages.error(request, "Recruiter matching query does not exist.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
    return render(request, "main/employer/emp_job.html")

#! EMPLOYER JOB_LIST: =======================================================
def job_list(request):
    employer = Employers.objects.get(user=request.user)
    job = Job.objects.filter(employers=employer)
    context={
        'job':job
    }
    return render(request, "main/employer/job_list.html" ,context)

#! EMPLOYER EDIT_JOB_DETAILS: ==================================================
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
            return redirect('job_list')
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

#! CANDIDATELIST: ==========================================================
def candidatelist(request):
    data = Apply.objects.all()
    context={
        "data":data
    }
    return render(request, 'main/employer/candidatelist.html', context)
