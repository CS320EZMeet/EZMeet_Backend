from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import findUser
import json
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
@csrf_exempt
def get(request):
    if request.method == 'GET':
        body = request.body
        if body:
            body = json.loads(body)
            userObj = findUser(body['userName'])
            if userObj:
                return JsonResponse({"status": 200, 'success': True, 'data': userObj, 'message': 'User found'})
            else:
                return JsonResponse({"status": 404, 'success': False, 'data': None, 'message': 'User not found'})
        else:
            return JsonResponse({"status": 400, 'success': False, 'message': "Invalid request, missing request body"})
    else:    
        return JsonResponse({'status': 405,'success': False, 'message': 'This endpoint only supports GET requests.'})
