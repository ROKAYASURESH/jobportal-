from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date
from job.models import *
from django.contrib.auth.forms import PasswordChangeForm

from datetime import datetime, timedelta

from django.utils import timezone

from job.form import AdminProfileUpdateForm, AdminJobseekerUpdateForm, AdminEmployerUpdateForm

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


#! JOBSEEKER AND EMPLOYER REGISTER LINK:
def JOB_USER(request):
    return render(request, 'base/common.html')

#! JOBSEEKER HOME PAGE: ========================
def HOME(request):
    user = request.user
    job = Job.objects.all()
    list = []

    if user.is_authenticated:
        try:
            student = JobSeekers.objects.get(user=user)
            data = Apply.objects.filter(student=student)
            for i in data:
                list.append(i.job.id)
        except JobSeekers.DoesNotExist:
            list = []
    else:
        list = []  # Ensure list is empty if the user is not logged in

    context = {
        'job': job,
        'list': list,
    }
    return render(request, 'main/home.html', context)

#! JOBSEEKER FIND_JOB PAGE: =======================
def JOB(request):
    # if not request.user.is_authenticated:
    #     return redirect('user_login')
    user = request.user
    job_type = Job_type.objects.all()
    label = Experience.objects.all()
    jobs = Job.objects.all()
    job =Job.objects.all().count()

    list = []
    if user.is_authenticated:
        try:
            student = JobSeekers.objects.get(user=user)
            data = Apply.objects.filter(student=student)
            for i in data:
                list.append(i.job.id)
        except JobSeekers.DoesNotExist:
            list = []
    else:
        list = []  # Ensure list is empty if the user is not logged in

    context={
        'job_type':job_type,
        'jobs':jobs,
        'job':job,
        'label':label,
        'list':list
    }
    return render(request, 'main/job.html', context)

#! JOBSEEKER JOB_TYPE AND EXPERIENCE FIND Through Check_box AJAX filter:===
def filter_data(request):
    job_type=request.GET.getlist('job_type[]')
    experience_ids = request.GET.getlist('experience[]')
    location = request.GET.get('location')
    title = request.GET.get('title')
    if title:
        job = Job.objects.filter(title=title)
    elif location:
        job = Job.objects.filter(location=location)
    elif job_type:
        job=Job.objects.filter(job_type__id__in =job_type).order_by('-id')
    elif experience_ids:
        job = Job.objects.filter(experience__id__in=experience_ids)
    else:
        job= Job.objects.all().order_by('-id')

    t = render_to_string('ajax/job.html', {'job':job})
    return JsonResponse({'data': t})

#! Remaning Days AJAX: ====================================
def filter_jobs_by_end_date(request):
    if request.method == 'GET':
        days_filter = int(request.GET.get('days', 0))
        target_date = date.today() - timedelta(days=days_filter)
        filtered_jobs = Job.objects.filter(creationdate__gte=target_date)
        
        jobs_data = []
        for job in filtered_jobs:
            jobs_data.append({
                'title': job.title,
                'location': job.location,
                'remaining_days': job.remaining_days(),
                'end_date': job.end_date.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({'jobs': jobs_data})

#! JOBSEEKER ABOUT PAGE: =======================   
def ABOUT(request):
    return render(request, 'main/about.html')

#! JOBSEEKER CONTACT PAGE: =======================
def CONTACT(request):
    return render(request, 'main/contact.html')

# #! JOBSEEKER JOB_DETAIL PAGE: =======================
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
#! JOBSEEKER SIGNUP:==============================
def SIGN_UP(request):
    if request.method == "POST" and request.FILES:
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        contact = request.POST['contact']
        gender = request.POST['gender']

        try:
            validate_password(password)            
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'auth/user_auth/user_signup.html', {
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                    'contact': contact,
                    'gender':gender ,
                } )
            
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already exists!")
                return render(request, 'auth/user_auth/user_signup.html', {
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                    'contact': contact,
                    'gender':gender ,
                } )
            
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            JobSeekers.objects.create(user=user, mobile=contact, image=image, gender=gender, is_student=True)
            messages.success(request, f'Registration successful, {firstname}! Welcome JobPortal')
            return redirect('user_login')
        
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('user_signup')

    return render(request, 'auth/user_auth/user_signup.html')

#! JOBSEEKER LOGIN: ==============================================
def USER_LOGIN(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user1 = JobSeekers.objects.get(user=user)
                if user1.is_student:
                    login(request, user)
                    messages.success(request, f'You have successfully logged in {username}')
                    return redirect('home')

                else:
                    messages.error(request, 'Invalid username or password.')
                    return redirect('user_login')

            except:
                messages.error(request, 'Invalid username or password.')
                return redirect('user_login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('user_login')
    return render(request, 'auth/user_auth/user_login.html')

#! JOBSEEKER LOGOUT: ==================================================
def USER_LOGOUT(request):
    logout(request)
    messages.success(request, 'You have successfully logged out,')
    return redirect('user_login')

#! JOBSEEKER PROFILE: =================================================
def user_profile(request):
    # Get or create the JobSeekers profile for the current user
    profile, created = JobSeekers.objects.get_or_create(user=request.user)
    profile_form = AdminJobseekerUpdateForm(instance=profile)

    if request.method == "POST":
        profile_form = AdminJobseekerUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_profile')

    context = {
        'profile_form': profile_form,
        'user': request.user,
        'profile': profile,  # Updated to directly pass the profile object
    }
    return render(request, "main/user_profile.html", context)

#! JOBSEEKER PASSWORD CHANGE: ==============================================
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

#! EMPLOYER APPLY fOR JOB:=====================================
def apply(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user
    today_date = timezone.now().date()

    # Check if the student profile exists
    student = JobSeekers.objects.filter(user=user).first()
    if not student:
        messages.error(request, 'Student profile not found.')
        return redirect('home')  # Redirect to an error page or some appropriate URL

    # Check if the job exists
    job = Job.objects.filter(id=id).first()  # Changed to Job from JobSeekers
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
