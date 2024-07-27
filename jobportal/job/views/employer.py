from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from job.models import *
from django.contrib.auth.forms import PasswordChangeForm
from job.form import AdminEmployerUpdateForm

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.template.loader import render_to_string

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
            Employers.objects.create(user=user, mobile=contact, company=company, image=image, is_employer = True, status='pending')
            messages.success(request, f'Registration successful, {firstname}! Welcome JopPortal')
            # Subject and message for the admin
            admin_subject = f'New Employer Registration: {firstname} {lastname}'
            admin_message = f"Hello Admin,\n\nA new employer has just registered on JobPortal. Here are the details:\n\nName: {firstname} {lastname}\nEmail: {email}\nContact: {contact}\nCompany: {company}\n\nPlease review their information and approve their account if everything is in order.\n\nBest regards,\nJobPortal Team"
            from_email = email  # Use user's email as the sender
            # Replace with your own email
            to_admin = ['sureshrokaya@ismt.edu.np']

            # Subject and message for the user
            user_subject = f'Welcome to JobPortal, {firstname}!'
            user_message = f"Dear {firstname},\n\nThank you for registering as an employer on JobPortal. We are excited to have you join our community.\n\nOur team is currently reviewing your registration details. You will receive an update once your account has been approved.\n\nIn the meantime, feel free to explore our platform and get ready to post your job vacancies.\n\nBest regards,\nJobPortal Team"
            to_user = [email]

         
            # Send email to admin
            send_mail(admin_subject, admin_message, from_email, to_admin)
            # Send confirmation email to user
            send_mail(user_subject, user_message, from_email, to_user)
            return redirect('employer_login')  # Replace 'dashboard' with the name of your success page URL pattern
           
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
    if request.method == "POST":
        job_title = request.POST['job_title']
        vacency = request.POST['vacency']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        image = request.FILES['image']
        des = request.POST['desc']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skill']
        
        employer = Employers.objects.get(user=request.user)
        
        try:
            job = Job.objects.create(
                employers=employer, title=job_title, vacency=vacency, 
                end_date=end_date, salary=salary, image=image, des=des, 
                experience=experience, location=location, skills=skills
            )
            messages.success(request, 'Job Detail has been added')

            # Send email to job seekers
            job_seekers = JobSeekers.objects.all()
            recipient_list = [job_seeker.user.username for job_seeker in job_seekers if job_seeker.user.username]
            
            send_mail(
                subject='New Job Posting: ' + job_title,
                message=f'A new job "{job_title}" has been posted. by {employer.user.first_name} {employer.user.last_name} Check it out!',
                from_email='your-email@example.com',
                recipient_list=recipient_list,
                fail_silently=False,
            )
            
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
        vacency= request.POST['vacency']
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
        
        if vacency:
            job.vacency=vacency
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
