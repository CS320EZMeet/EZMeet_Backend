from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
### functions or classes are mappted to urls

#welcome page
def index(request):
    return HttpResponse("Welcome to EZMeet")

def login(request):
    return HttpResponse("Login to EZMeet account")

def create(request):
    return HttpResponse("Create an EZMeet account")
