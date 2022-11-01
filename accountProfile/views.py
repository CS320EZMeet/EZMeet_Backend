from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import findUser
import json
from django.contrib.auth.models import User
#from rest_framework import viewsets
#from .serializers import UserSerializer

# Create your views here.

#welcome page
def index(request):
    return HttpResponse("Welcome page to Account profile")

# A possible template for creating a user from front-end form, and placing in DB
def createUser(request, userObj):
    if request.method == 'PUT':
        if findUser(user.username):
            return HttpResponse('That username is taken. Please try another.')
        else:
            user = User.objects.create_user(
                username=userObj.username,
                email=userObj.email,
                password=userObj.password
            )
            # I think we would then want to CREATE TABLE for user - unsure how to proceed, function in models?
            return JsonResponse(data = {'status': 200,'success': True, 'data': userObj, 'message': 'User created.'}, status = 405)
    else:
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports PUT requests.'}, status = 405)

# Should have login functionality, like createUser for sign-up
def login(request):
    return

#does user want to make their location be private/public?
def showLocation(request):
    return 

#user's preference list of activities they want to do
def preferences(request):
    return

#name, addresses, profile pic?, gender, age?
@csrf_exempt
def get(request, userName):
    if request.method == 'GET':
        userObj = findUser(userName)
        if userObj:
            return JsonResponse(data = {"status": 200, 'success': True, 'data': userObj, 'message': 'User found'}, status = 200)
        else:
            return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User not found'}, status = 404)
    else:    
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports GET requests.'}, status = 405)
