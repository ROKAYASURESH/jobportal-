from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date
from .models import *
from datetime import datetime, timedelta

from .form import AdminProfileUpdateForm, AdminJobseekerUpdateForm, AdminEmployerUpdateForm

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

'''=========User and Employer Commmon link=============================''' 
def JOB_USER(request):
    return render(request, 'base/common.html')

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

# for Check box filter
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

# Remaning Days
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

# User_Login
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

# Logout
def USER_LOGOUT(request):
    logout(request)
    messages.success(request, 'You have successfully logged out,')
    return redirect('user_login')

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

# ==================END========================

'''=================================================================
                    EMPLOYER START
   =================================================================
'''

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
def Employer_LOGOUT(request):
    logout(request)
    messages.success(request, 'You have successfully logged out,')
    return redirect('employer_login')
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
# Recrutier_login
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

'''=================================================================
                    ADMIN
   =================================================================
'''
# ADMIN_DASHBOARD:
def ADMIN_DASHBOARD(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    employer=Employers.objects.all().count()
    Jobseeker=JobSeekers.objects.all().count()
    pending =Employers.objects.filter(status='pending').count()
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
                messages.success(request,f'You have successfully logged in {username}')
                return redirect('admin_dashboard')
            else:
                messages.error(request,f'Invalid Creditanial Try Again')
                return redirect('admin_login')
        except:
            messages.error(request,f'Invalid Creditanial Try Again')
            return redirect('admin_login')
    return render(request, 'auth/admin_auth/admin_login.html')

# Logout
def ADMIN_LOGOUT(request):
    logout(request)
    return redirect('admin_login')

# 
def admin_profile(request):
    profile,created=AdminProfile.objects.get_or_create(user=request.user)
    profile_form=AdminProfileUpdateForm(instance=profile)

    if request.method=="POST":
        profile_form=AdminProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('admin_profile')

    context={
        'profile_form':profile_form,
        'user':request.user,
        'profile':request.user.adminprofile,
    }
    return render(request, "auth/admin_auth/admin_profile.html", context)

def admin_password_change(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('admin_login')
            else:
                messages.error(request, "Your old password was entered incorrectly. Please enter it again.")
        except User.DoesNotExist:
            messages.error(request, "Something went wrong. User does not exist.")
    else:
        messages.error(request, "Invalid request method.")

    return render(request, "auth/admin_auth/admin_password_change.html")

# User Data
def VIEWS_USERS(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = JobSeekers.objects.all()
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
    data =Employers.objects.filter(status='pending')
    context={
        'data':data
    }
    return render(request, "main/admin/recruiter_pending.html", context)

# Change_Status form
def CHANGE_STATUS(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    error=''
    employers =Employers.objects.get(id=id)
    if request.method == "POST":
        status=request.POST['status']
        employers.status = status
        try:
            employers.save()
            error='no'
        except:
            error='yes'
    context={
        'employers':employers,
        'error':error
    }
    return render(request, "main/admin/change_status.html", context)


# Employer Accepted Data Show
def emplpyer_accept(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.filter(status='Accept')
    context={
        'data':data
    }
    return render(request, "main/admin/employer_accept.html", context)

# Employer Reject Data Show
def employer_reject(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.filter(status='Reject')
    context={
        'data':data
    }
    return render(request, "main/admin/employer_reject.html", context)

# Employer employer_all Data Show
def employer_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.all()
    context={
        'data':data
    }
    return render(request, "main/admin/employer_all.html", context)


def DELETE_EMPLOYER(request, id):
    data =User.objects.get(id=id)
    data.delete()
    return redirect('employer_all')



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


def job_list(request):
    employer = Employers.objects.get(user=request.user)
    job = Job.objects.filter(employers=employer)
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



from django.utils import timezone
# APPLY for a job
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
