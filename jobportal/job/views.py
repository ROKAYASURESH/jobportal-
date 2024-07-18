from django.shortcuts import render

# Create your views here.
def HOME(request):
    return render(request, 'main/home.html')
def JOB(request):
    return render(request, 'main/job.html')
def ABOUT(request):
    return render(request, 'main/about.html')
def CONTACT(request):
    return render(request, 'main/contact.html')
def JOB_DETAILS(request):
    return render(request, 'main/job_details.html')