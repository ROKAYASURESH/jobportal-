from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from job.models import *
from job.form import AdminProfileUpdateForm


#! ADMIN_DASHBOARD: ======================================
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

#! ADMIN LOGIN: ===================================================
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

#! ADMIN LOGOUT: ====================================================
def ADMIN_LOGOUT(request):
    logout(request)
    return redirect('admin_login')


#! ADMIN PROFILE: ================================================================
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

#! ADMIN PASSWORD CHANGE: ===================================================
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

#! JOBSEEKER DATA SHOW ====================================
def VIEWS_USERS(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = JobSeekers.objects.all()
    context={
        'data':data
    }
    return render(request, "main/admin/views_user.html", context)

#! JOBSEEKER DATA DELETE: ===========================================
def DELETE_USER(request, id):
    data =User.objects.get(id=id)
    data.delete()
    return redirect('views_user')

#! EMPLOYER ACCOUNT PENDING DATA SHOW: ===========
def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.filter(status='pending')
    context={
        'data':data
    }
    return render(request, "main/admin/recruiter_pending.html", context)

#! EMPLOYER PENDING ACCOUNT STATUS CHANGE FORM: ===
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


#! EMPLOYER ACCEPTED DATA SHOW: ==============================
def emplpyer_accept(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.filter(status='Accept')
    context={
        'data':data
    }
    return render(request, "main/admin/employer_accept.html", context)

#! EMPLOYER REJECT DATAS SHOW: ========================
def employer_reject(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.filter(status='Reject')
    context={
        'data':data
    }
    return render(request, "main/admin/employer_reject.html", context)

#! EMPLOYER ALL DATA SHOW: ================================================
def employer_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data =Employers.objects.all()
    context={
        'data':data
    }
    return render(request, "main/admin/employer_all.html", context)

#! EMPLOYER DATA DELETE: ==================
def DELETE_EMPLOYER(request, id):
    data =User.objects.get(id=id)
    data.delete()
    return redirect('employer_all')

#! ALL CANDIDATED LIST: ==============
def all_applied_list(request):
    all = Apply.objects.all()
    context={
        "all":all
    }
    return render(request, 'main/admin/all_applied_list.html', context)


