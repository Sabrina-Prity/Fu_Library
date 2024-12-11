from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name = 'registration'),
    path('login/', views.user_login, name = 'user_login'),
    path('logout/', views.user_logout, name = 'user_logout'),
    path('profile/', views.user_profile, name = 'profile'),
    path('profile/edit/', views.edit_profile, name = 'edit_profile'),
    path('profile/edit/pass_change/', views.change_pass, name = 'pass_change'),
]