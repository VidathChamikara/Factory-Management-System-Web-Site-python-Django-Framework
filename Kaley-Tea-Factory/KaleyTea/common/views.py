from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

#Home Navigations------------------------------------------------------------------------------------------


def home(request):

    return render(request, 'Home/home.html')
