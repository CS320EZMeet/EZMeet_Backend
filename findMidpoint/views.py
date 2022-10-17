from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
### functions or classes are mappted to urls

#welcome page
def index(request):
    return HttpResponse("Welcome page to findMidpoint")

def calcMidpoint(request):
    return

def createRecommendationList(request):
    return


