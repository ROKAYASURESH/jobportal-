from django import forms
from .models import AdminProfile

class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['profile_picture', 'phone_number', 'address']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number.'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address.'}),
        }
