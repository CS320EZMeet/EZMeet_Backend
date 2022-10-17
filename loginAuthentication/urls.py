from django.urls import path
from . import views

#maps views to url

### local:8000/loginAuthentication/index
urlpatterns = [
    path('index', views.index),
    path('login', views.login),
    path('create', views.create)
]