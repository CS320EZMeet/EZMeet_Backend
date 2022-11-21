from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import groupUsers, userLocations

#welcome page
def index(request):
    return HttpResponse("Welcome page to findMidpoint")

def calcMidpoint(locations):
    length = len(locations)
    sumX = 0
    sumY = 0
    for pt in locations:
        sumX += pt[0]
        sumY += pt[1]

    return [sumX / length, sumY / length]

def getMidpoint(request, groupID):
    try:
        if request.method == 'GET':
            users = groupUsers(groupID)
            if users == None:
                return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'Group not found'}, status = 404)
            else:
                locations = userLocations(users)
                if locations == None:
                    return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User\'s location is not set'}, status = 404)
                else:
                    midpoint = calcMidpoint(locations)
                    return JsonResponse(data = {"status": 200, 'success': True, 'data': {'Latitude': midpoint[0], 'Longitude': midpoint[1]}, 'message': 'Midpoint Calculated'}, status = 200)
        else:    
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports GET requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)

def createRecommendationList(request):
    return


