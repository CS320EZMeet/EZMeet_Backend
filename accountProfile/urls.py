from django.db import models
from django.urls import include, path
from accountProfile import views

urlpatterns = [
    path('get/<str:userName>/', views.get),
    path('login/<str:userName>/', views.login),
    path('register/<str:userName>/', views.registerUser),
    path('update/<str:userName>/', views.updateUser),
    path('getLocation/<str:userName>/', views.getLocation),
    path('setLocation/<str:userName>/', views.setLocation),
]