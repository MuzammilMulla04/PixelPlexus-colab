from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Profile

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full border text-white placeholder-gray-400 border-gray-300 bg-neutral-600 rounded-md p-2 focus:outline-none focus:ring focus:ring-gray-300 focus:transition-transform transform scale-100 focus:scale-105', 
            'placeholder': '********'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full border text-white placeholder-gray-400 border-gray-300 bg-neutral-600 rounded-md p-2 focus:outline-none focus:ring focus:ring-gray-300 focus:transition-transform transform scale-100 focus:scale-105', 
            'placeholder': '********'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border text-white placeholder-gray-400 border-gray-300 bg-neutral-600 rounded-md p-2 focus:outline-none focus:ring focus:ring-gray-300 focus:transition-transform transform scale-100 focus:scale-105', 
                'placeholder': 'user@123'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border text-white placeholder-gray-400 border-gray-300 bg-neutral-600 rounded-md p-2 focus:outline-none focus:ring focus:ring-gray-300 focus:transition-transform transform scale-100 focus:scale-105', 
                'placeholder': 'user@gmail.com'
            }),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'mt-1 block w-full border text-white placeholder-gray-400 border-gray-300 bg-neutral-600 rounded-md p-2 focus:outline-none focus:ring focus:ring-gray-300 focus:transition-transform transform scale-100 focus:scale-105',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border text-white placeholder-gray-400 border-gray-300 bg-neutral-600 rounded-md p-2 focus:outline-none focus:ring focus:ring-gray-300 focus:transition-transform transform scale-100 focus:scale-105',
            }),
        }