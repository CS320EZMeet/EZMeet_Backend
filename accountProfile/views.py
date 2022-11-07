from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import findUser, createUser
# Modules we may implement:
# import simplejson as json
# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from .serializers import UserSerializer

#welcome page
def index(request):
    return HttpResponse("Welcome page to Account profile")

# A possible template for creating a user from front-end form, and placing in DB
def registerUser(request, user):
    if request.method == 'PUT':
        if findUser(user.username):
            return JsonResponse(data = {'status': 409, 'success': False, 'message': 'That username is taken. Please try another.'}, status = 409)
        else:
            # Unclear if this will be used
            # django_user = User.objects.create_user(
            #     username=userObj.username,
            #     email=userObj.email,
            #     password=userObj.password
            # )
            createUser(user)
            return JsonResponse(data = {'status': 200,'success': True, 'data': user, 'message': 'User created.'}, status = 200)
    else:
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports PUT requests.'}, status = 405)

# Password will be properly verified in final release
@csrf_exempt
def login(request, userName):
    if request.method == 'POST':
        user = findUser(userName)
        if user is not None:
            #if user.password == password:
            return JsonResponse(data = {'status': 200, 'success': True, 'data': user, 'message': 'Logged-in.'}, status = 200)
            #else:
                #return JsonResponse(data = {'status': 401, 'success': False, 'message': 'Incorrect Password Entered. Please try again.'}, status = 200)
        else:
            return JsonResponse(data = {'status': 200, 'success': False, 'message': 'That account doesn\'t exist. Create a new account.'}, status = 200)
    else:
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports POST requests.'}, status = 405)

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
