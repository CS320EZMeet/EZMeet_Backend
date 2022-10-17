from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
### functions or classes are mappted to urls

#welcome page
def index(request):
    return HttpResponse("welcome page to createGroup")


def createSharableLink(request):
    return

#how many ppl allowed to join the group? etc
def groupSettings(request):
    return

