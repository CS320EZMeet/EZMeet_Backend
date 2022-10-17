from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
### functions or classes are mappted to urls

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
def basicInfo(request):
    return
