from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date
from job.models import *
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from django.utils import timezone
from job.form import AdminJobseekerUpdateForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all notifications as read
    notifications.update(is_read=True)
    
    return render(request, 'main/notifications.html', {'notifications': notifications})

def notification_count(request):
    if request.user.is_authenticated:
        return {'notification_count': Notification.objects.filter(user=request.user, is_read=False).count()}
    return {'notification_count': 0}

#! JOBSEEKER AND EMPLOYER REGISTER LINK:
def JOB_USER(request):
    return render(request, 'base/common.html')

#! JOBSEEKER HOME PAGE: ========================
from django.db.models import Count
def HOME(request):
    employers = Employers.objects.annotate(job_count=Count('job')).all().order_by('-id')[:8]
    user = request.user
    job = Job.objects.all().order_by('-id')

    paginator=Paginator(job, 4) #number of items to display per page
    page_num=request.GET.get('page') #current page /127.0.0.1:8000/?page=1
    job=paginator.get_page(page_num)#fetch the data from current page
    total=job.paginator.num_pages #3
    
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
        'job':job,
        'total':total,
        'num':[i+1 for i in range(total)],#for i in range(3):#  [1,2,3],

        'employers': employers
    }
    return render(request, 'main/home.html', context)

# ! Comapay

def copmany(request, id):
    company=Employers.objects.get(id=id)

    return render(request, 'main/company.html', {
        'company': company,
       
    })



#! JOBSEEKER FIND_JOB PAGE: =======================
from django.core.paginator import Paginator

def JOB(request):
    # if not request.user.is_authenticated:
    #     return redirect('user_login')
    
    user = request.user
    job_type = Job_type.objects.all().order_by('-id')
    label = Experience.objects.all().order_by('-id')
    jobs = Job.objects.all().order_by('-id')
    job =Job.objects.all().count()

    paginator=Paginator(jobs, 5) #number of items to display per page
    page_num=request.GET.get('page') #current page /127.0.0.1:8000/?page=1
    jobs=paginator.get_page(page_num)#fetch the data from current page
    total=jobs.paginator.num_pages #3

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
        'list':list,
       
        'total':total,
        'num':[i+1 for i in range(total)]#for i in range(3):#  [1,2,3]
       

    }
    return render(request, 'main/job.html', context)


def SEARCH_JOB(request):
   
    query = request.GET['query']
    jobs = Job.objects.filter(title__icontains = query)
    print(jobs)
    context = {
        'jobs':jobs,
    }
    return render(request,'search/search.html',context)
#! JOBSEEKER JOB_TYPE AND EXPERIENCE FIND Through Check_box AJAX filter:===
def filter_data(request):
    jobcount =Job.objects.all().count()
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

    t = render_to_string('ajax/job.html', {'job':job, 'jobcount':jobcount})
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
    required_knowledge_list = job.required_knowledge_set.all()[:5]  # Limit to 5
    educationexperience_list = job.educationexperience_set.all()[:5]  # Limit to 5

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    saved_jobs = user_profile.saved_jobs.all()
    return render(request, 'main/job_details.html', {
        'job': job,
        'saved_jobs': saved_jobs,
        'required_knowledge_list': required_knowledge_list,
        'educationexperience_list':educationexperience_list
    })
 


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
            
            users = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            JobSeekers.objects.create(user=users, mobile=contact, image=image, gender=gender, is_student=True)
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
                    return render(request, 'auth/user_auth/user_login.html', {
                    'email': username,
                } )

            except:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'auth/user_auth/user_login.html', {
                    'email': username,
                } )
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'auth/user_auth/user_login.html', {
                    'email': username,
                } )
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
    elif job.creationdate > today_date:
        messages.error(request, 'Job not open yet')
    else:
        if request.method == "POST":
            cv = request.FILES.get('cv')
            if cv:
                Apply.objects.create(student=student, job=job, cv=cv, applydate=today_date)
                # Remove the job from the user's saved list
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                if job in user_profile.saved_jobs.all():
                    user_profile.saved_jobs.remove(job)
                
                messages.success(request, 'Application submitted successfully.')
                return redirect("saved_jobs_view")  # Redirect back to the saved jobs view
            else:
                messages.error(request, 'CV file is missing.')
    return render(request, "main/apply.html")


def save_job_for_later(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.saved_jobs.add(job)
    return redirect('home')

def saved_jobs_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    saved_jobs = user_profile.saved_jobs.all()
    return render(request, 'main/laterlist.html', {
        'saved_jobs': saved_jobs
    })
   