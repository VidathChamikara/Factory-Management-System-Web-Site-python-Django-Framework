from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile-update'),

]