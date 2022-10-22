from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.auth.models import User
#from rest_framework import viewsets
#from .serializers import UserSerializer

# Create your views here.

#welcome page
def index(request):
    return HttpResponse("Welcome page to Account profile")

#does user want to make their location be private/public?
def showLocation(request):
    return 

#user's preference list of activities they want to do
def preferences(request):
    return

#name, addresses, profile pic?, gender, age?
def get(request):
    if request.method == 'POST':
        return HttpResponse("This is a POST request.")
    else:    
        return HttpResponse("This is not a POST request.")
