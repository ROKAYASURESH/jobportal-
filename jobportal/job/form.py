from django import forms
from .models import AdminProfile, JobSeekers, Employers

class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['profile_picture', 'phone_number', 'address']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number.'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address.'}),
        }
class AdminJobseekerUpdateForm(forms.ModelForm):
    class Meta:
        model = JobSeekers
        fields = ['mobile', 'image', 'gender']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number.'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address.'}),
        }

class AdminEmployerUpdateForm(forms.ModelForm):
    class Meta:
        model = JobSeekers
        fields = ['mobile', 'image', 'company', 'gender']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number.'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Gender.'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your company.'}),
        }

