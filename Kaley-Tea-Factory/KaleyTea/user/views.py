from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as logouts
from django.contrib.auth import login as logins
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm


# Create your views here

# ----------------------------Create User Registration Form------------------------------------------
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'InventoryUser/register.html', {'form': form})


# ----------------------------Create User Login Form------------------------------------------
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            logins(request, user)
            return redirect('dashboard-index')
    else:
        form = AuthenticationForm()
    return render(request, 'InventoryUser/login.html', {'form': form})


# ----------------------------Create User Logout Form------------------------------------------
def logout(request):
    if request.method == 'POST':
        logouts(request)
        return redirect('dashboard-index')


# ----------------------------Create User Profile Form------------------------------------------

def profile(request):
    return render(request, 'InventoryUser/profile.html')


# ----------------------------User Profile Form Update------------------------------------------

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard-staff')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,

    }
    return render(request, 'InventoryUser/profile_update.html', context)
