from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Mete:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'phone', 'first_name', 'last_name', 'address']
