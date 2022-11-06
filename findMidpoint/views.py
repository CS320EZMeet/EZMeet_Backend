from django.shortcuts import render
from django.http import HttpResponse
from .models import getLocation

# Create your views here.
### functions or classes are mappted to urls

#welcome page
def index(request):
    return HttpResponse("Welcome page to findMidpoint")

# calculates the centroid of a set of points
# showMidpoint(request: HTTP request, group: user[]) => [latitude: number, longitude: number]
def showMidpoint(request, group):
    # In the future, may want to check for type of HTTP request
    # list of dictionaries, one for each member of group:
    locs = []
    for user in group:
        loc = getLocation(user.username)
        if loc == None:
            '1 User not found.'
        else:
            locs.append(loc)
    sumX = 0
    sumY = 0
    length = len(locs)
    
    for pt in locs:
        sumX += pt.latitude
        sumY += pt.longitude

    return [sumX / length, sumY / length]

def createRecommendationList(request):
    return


