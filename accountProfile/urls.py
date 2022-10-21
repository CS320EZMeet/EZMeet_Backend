from django.db import models
from django.urls import include, path
from accountProfile import views

urlpatterns = [
    path('', views.get),
]