from django.db import models
from django.urls import include, path
from accountProfile import views

urlpatterns = [
    path('get/<str:userName>/', views.get),
    path('login/<str:userName>/', views.login),
]