from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

# Registers a user
@csrf_exempt
def registerUser(request, userName):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = {'userName': userName, 'email': body['email'], 'password': body['password']}
        if findUser(userName) is None:
            createUser(user)
            return JsonResponse(data = {'status': 200,'success': True, 'data': user, 'message': 'User created.'}, status = 200)
        else:
            return JsonResponse(data = {'status': 409, 'success': False, 'message': 'That username is taken. Please try another.'}, status = 409)
    else:
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports PUT requests.'}, status = 405)

# Update user details
@csrf_exempt
def updateUser(request, userName):
    if request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body is None or body['user'] is None:
            return JsonResponse(data = {'status': 401, 'success': False, 'message': 'Missing necessary data to complete request.'}, status = 401)
        
        user = body['user']    
        if findUser(user['userName']) is None:
            return JsonResponse(data = {'status': 200, 'success': False, 'message': 'That account doesn\'t exist.'}, status = 200)
        
        newUser = updateFields(user)

        return JsonResponse(data = {'status': 200, 'success': True, 'data': newUser, 'message': 'User updated.'}, status = 200)
    else:
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports PUT requests.'}, status = 405)
    
# Login to account
@csrf_exempt
def login(request, userName):
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        if request.method == 'POST':
            password = body_data['password']
            if password is None or password == '':
                return JsonResponse(data = {'status': 401, 'success': False, 'message': 'No password received.'}, status = 401)
            user = findUser(userName)
            if user is not None:
                if user['password'] == password:
                    return JsonResponse(data = {'status': 200, 'success': True, 'data': user, 'message': 'Logged-in.'}, status = 200)
                else:
                    return JsonResponse(data = {'status': 401, 'success': False, 'message': 'Incorrect Password Entered. Please try again.'}, status = 401)
            else:
                return JsonResponse(data = {'status': 200, 'success': False, 'message': 'That account doesn\'t exist. Create a new account.'}, status = 200)
        else:
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports POST requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)

# Get user's location
@csrf_exempt
def getLocation(request, userName):
    loc = findLocation(userName)
    if loc is None:
        return JsonResponse(data = {'status': 200, 'success': False, 'message': 'That account doesn\'t exist.'}, status = 200)
    else:
        return JsonResponse(data = {'status': 200, 'success': True, 'data': loc, 'message': 'Location fetched.'}, status = 200)

# Set user's location
@csrf_exempt
def setLocation(request, userName):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = updateLocation(userName, body['latitude'], body['longitude'], body['address'])
    if user is None:
        return JsonResponse(data = {'status': 200, 'success': False, 'message': 'That account doesn\'t exist.'}, status = 200)
    else:
        return JsonResponse(data = {'status': 200, 'success': True, 'data': user, 'message': 'Preferences fetched.'}, status = 200)

#Get a user's data
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