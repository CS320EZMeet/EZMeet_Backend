from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import groupUsers, userLocations, userPreferences, matchPreferenceIDtoBools
import requests
from collections import defaultdict
from EZmeet import settings


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
            elif len(users) == 1:
                return JsonResponse(data = {"status": 400, 'success': False, 'data': None, 'message': 'Cannot find midpoint with just one user'}, status = 400)
            else:
                locations = userLocations(users)
                if locations == None:
                    return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User\'s location is not set; cannot calculate places without user\'s location'}, status = 404)
                else:
                    midpoint = calcMidpoint(locations)
                    print(midpoint)
                    # list of prefIDs
                    preferences = userPreferences(users)
                    if preferences == None or len(preferences) == 0:
                        return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User Preference not found'}, status = 404)
                    else:
                        types = findCommonPreferences(preferences)
                        locations = createRecommendationList(midpoint, types)
                    return JsonResponse(data = {"status": 200, 'success': True, 'data': locations, 'message': 'List of Places Generated'}, status = 200)
        else:    
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports GET requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)

#helper function for findCommonPreferences()
def column(matrix, i):
    return [row[i] for row in matrix]

def findCommonPreferences(preferences):
    matrix = defaultdict(int)
    for pref in preferences:
        prefBools = matchPreferenceIDtoBools(pref)
        (RestaurantBar, Nature, Museums, Entertainment, Shopping) = prefBools
        if RestaurantBar:
            matrix['restaurantBar'] += 1
        if Nature:
            matrix['nature'] += 1
        if Museums:
            matrix['museum'] +=1
        if Entertainment:
            matrix['entertainment'] +=1
        if Shopping:
            matrix['shopping'] += 1
        res = {key: value/len(preferences) for key, value in matrix.items()}
        maxVal = max(res.values())
    keys = set([key for key, value in res.items() if value == maxVal])
    print(keys)
    return keys

def createRecommendationList(midpoint, types):
        restaurantBar = ["restaurant", "bar", "cafe", "night_club"]
        nature = ["campground", "park"]
        shopping = ["clothing_store", "department_store", "shopping_mall"]
        entertainment = ["amusement_park", "aquarium", "bowling_alley", "movie_theater", "tourist_attraction", "zoo"]
        museum = ["museum", "art_gallery"]
        locations = []
        #we only want to return 10 places
        for t in types:
            if len(locations) > 10:
                break
            if t == "restaurantBar":
                for type in restaurantBar:
                    loc = findPlacesHepler(midpoint, type)
                    print(loc)
                    locations += loc
                    if len(locations) > 10:
                        break
            elif t == "nature":
                for type in nature:
                    loc = findPlacesHepler(midpoint, type)
                    locations += loc
                    print(loc)

                    if len(locations) > 10:
                        break
            elif t == "shopping": 
                for type in shopping:
                    loc = findPlacesHepler(midpoint, type)
                    locations += loc
                    if len(locations) > 10:
                        break
            elif t == "entertainment":
                for type in entertainment:
                    loc = findPlacesHepler(midpoint, type)
                    locations += loc
                    if len(locations) > 10:
                        break
            elif t == "museum":
                for type in museum:
                    loc = findPlacesHepler(midpoint, type)
                    locations += loc
                    if len(locations) > 10:
                        break
        return locations

    
#will access google places API and return a list of tuples containing the place's fields(name, lat, long, address) based on the lat/long and the type
def findPlacesHepler(midpoint, type):
    API_KEY = settings.GOOGLE_API_KEY
    payload={}
    headers={}
    locations = []
    #make a request for the place details
    link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ str(midpoint[0]) + "," + str(midpoint[1]) + "&radius=20000&types=" + type + "&key=" + API_KEY
    places_result = requests.request("GET", link, headers=headers, data=payload)
    places_result = places_result.json()
    for places in places_result['results']:
        place_id = places["place_id"]

        #to access all fields
        url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + place_id + "&fields=name%2Cformatted_address%2Cgeometry&key=" + API_KEY
        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()
        response= response['result']
        # place_details = (places['name'], places['geometry']['location']['lat'], places['geometry']['location']['lng'], address)
        response_detals = (response['name'], response['geometry']['location']['lat'], response['geometry']['location']['lng'], response['formatted_address'])
        locations.append(response_detals)
    return locations
