from django.http import HttpResponse, JsonResponse
from .models import *
import requests
from collections import defaultdict
from EZmeet import settings
import math

#welcome page
def index(request):
    return HttpResponse("Welcome page to findMidpoint")

#helper function
def calcMidpoint(locations):
    length = len(locations)
    sumX = 0
    sumY = 0
    for pt in locations:
        sumX += pt[0]
        sumY += pt[1]

    return [sumX / length, sumY / length]

#main request
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
                    # list of prefIDs
                    preferences = userPreferences(users)
                    if preferences == None or len(preferences) == 0:
                        return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User Preference not found'}, status = 404)
                    else:
                        types = findCommonPreferences(preferences)
                        locations = createRecommendationList(midpoint, types)
                        if len(locations) < 10:
                            return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'Insufficient number of places found near the midpoint'}, status = 404)
                        else:
                            return JsonResponse(data = {"status": 200, 'success': True, 'data': locations[:10], 'message': 'List of Places Generated'}, status = 200)
        else:    
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports GET requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)

#helper function for findCommonPreferences()
def column(matrix, i):
    return [row[i] for row in matrix]

#helper
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
    return keys

#helper
def createRecommendationList(midpoint, types):
        restaurantBar = ["restaurant", "bar", "cafe", "night_club"]
        nature = ["campground"]
        shopping = ["clothing_store", "department_store", "shopping_mall"]
        entertainment = ["amusement_park", "aquarium", "bowling_alley", "movie_theater", "tourist_attraction", "zoo"]
        museum = ["museum", "art_gallery"]
        locations = []
        places_id = set()
        #default search is 1 mile radius
        miles = 1
        count = 0
        #max radius search is 128 miles we want to only grab 10 locations
        while len(locations) < 10 and miles <= 128:
            radius = getMeters(miles)
            for t in types:
                if len(locations) > 10:
                    break
                if t == "restaurantBar":
                    for type in restaurantBar:
                        loc, ids = findPlacesHepler(midpoint, type, radius, places_id)
                        locations += loc
                        places_id.update(ids)
                        if len(locations) > 10:
                            break
                elif t == "nature":
                    for type in nature:
                        loc, ids = findPlacesHepler(midpoint, type, radius, places_id)
                        locations += loc
                        print(loc)
                        places_id.update(ids)
                        if len(locations) > 10:
                            break
                elif t == "shopping": 
                    for type in shopping:
                        loc, ids = findPlacesHepler(midpoint, type, radius, places_id)
                        locations += loc
                        places_id.update(ids)
                        if len(locations) > 10:
                            break
                elif t == "entertainment":
                    for type in entertainment:
                        loc, ids = findPlacesHepler(midpoint, type, radius, places_id)
                        locations += loc
                        places_id.update(ids)
                        if len(locations) > 10:
                            break
                elif t == "museum":
                    for type in museum:
                        loc, ids = findPlacesHepler(midpoint, type, radius, places_id)
                        locations += loc
                        places_id.update(ids)
                        if len(locations) > 10:
                            break
            #increase the radius
            count += 1
            miles = math.pow(2, count)
        return locations

def getMeters(miles):
     return miles*1609.344

#will access google places API and return a list of tuples containing the place's fields(name, lat, long, address) based on the lat/long and the type
def findPlacesHepler(midpoint, type, radius, places_id_set):
    API_KEY = settings.GOOGLE_API_KEY
    payload={}
    headers={}
    locations = []
    #make a request for the place details
    link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ str(midpoint[0]) + "," + str(midpoint[1]) + "&radius=" + str(radius) + "&types=" + type + "&key=" + API_KEY
    
    places_result = requests.request("GET", link, headers=headers, data=payload)
    places_result = places_result.json()
    for places in places_result['results']:
        place_id = places["place_id"]

        #this is so it doesn't call the API again on places that's already been searched in the previous radius search
        if place_id in places_id_set:
            continue
        else:
            places_id_set.add(place_id)

            #to access all fields
            url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + place_id + "&fields=name%2Cformatted_address%2Cgeometry&key=" + API_KEY
            response = requests.request("GET", url, headers=headers, data=payload)

            response = response.json()
            response= response['result']
            response_details = (response['name'], response['geometry']['location']['lat'], response['geometry']['location']['lng'], response['formatted_address'])
            locations.append(response_details)
    return locations, places_id_set
