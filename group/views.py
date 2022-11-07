from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

# Create your views here.

def index(request):
    return HttpResponse("welcome to group page")

def groupDataHelper(groupID, users, locations):
    data = {'groupId': groupID}
    userObjects = []
    for i in range(len(users)):
        user = {}
        user['username'] = users[i]
        user['longitude'] = locations[i][1]
        user['latitude'] = locations[i][0]
        userObjects.append(user)
    data['users'] = userObjects
    return data

@csrf_exempt
def group(request, userName):
    try:
        if request.method == 'GET':
            groupID = userToGroupID(userName)
            if groupID == 'Null':
                return JsonResponse(data = {"status": 200, 'success': False, 'data': None, 'message': 'User not in a group'}, status = 200)
            elif groupID == None:
                return JsonResponse(data = {"status": 403, 'success': False, 'data': None, 'message': 'User not found'}, status = 403)
            else:
                users = groupUsers(groupID)
                if users == None:
                    return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'Group not found'}, status = 404)
                else:
                    locations = userLocations(users)
                    if locations == None:
                        return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User\'s location is not set'}, status = 404)
                    else:
                        return JsonResponse(data = {"status": 200, 'success': True, 'data': groupDataHelper(groupID, users, locations), 'message': 'Group found'}, status = 200)
        
        elif request.method == 'POST':
            groupID = userToGroupID(userName)
            if groupID == None:
                return JsonResponse(data = {"status": 403, 'success': False, 'data': None, 'message': 'User not found'}, status = 403)
            elif groupID == 'Null':
                groupID = createNewGroup(userName)
                success = updateUserGroup(userName, groupID)
                if success == None:
                    return JsonResponse(data = {"status": 500, 'success': False, 'data': None, 'message': 'Error creating group'}, status = 500)
                else:
                    return JsonResponse(data = {"status": 200, 'success': True, 'data': {'group_id': groupID}, 'message': 'new group successfully formed'}, status = 200)
            else:
                return JsonResponse(data = {"status": 200, 'success': False, 'data': None, 'message': 'User already in a group'}, status = 200)
        else:    
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports GET and POST requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)
    
@csrf_exempt
def groupJoin(request, groupID):
    try:
        if request.method == 'POST':
            body = request.body
            if body:
                body = json.loads(body)
                userName = body['userName']
                if userName == None:
                    return JsonResponse(data = {'status': 400,'success': False, 'message': 'userName not specified in body'}, status = 400)
            else:
                return JsonResponse(data = {'status': 400,'success': False, 'message': 'userName not specified in body'}, status = 400)
            userCheck = userToGroupID(userName)
            if userCheck == None:
                return JsonResponse(data = {"status": 403, 'success': False, 'data': None, 'message': 'User not found'}, status = 403)
            elif userCheck == 'Null':
                users = groupUsers(groupID)
                if users == None:
                    return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'Group not found'}, status = 404)
                elif len(users) == 5:
                    return JsonResponse(data = {"status": 200, 'success': False, 'data': None, 'message': 'Group is full'}, status = 200)
                else:
                    success = updateUserGroup(userName, groupID)
                    if success == None:
                        return JsonResponse(data = {"status": 500, 'success': False, 'data': None, 'message': 'Error updating groupID in users'}, status = 500)
                    else:
                        userNum = len(users)+1
                        success = updateGroup(userName, groupID, userNum)
                        if success == None:
                            return JsonResponse(data = {"status": 500, 'success': False, 'data': None, 'message': 'Error updating user in group'}, status = 500)
                        else:
                            return JsonResponse(data = {"status": 200, 'success': True, 'data': {'group_id': groupID}, 'message': 'User successfully joined group'}, status = 200)
            else:
                return JsonResponse(data = {"status": 200, 'success': False, 'data': None, 'message': 'User already in a group'}, status = 200)
        else:    
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports POST requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)

@csrf_exempt
def groupLeave(request, groupID):
    try:
        if request.method == 'POST':
            body = request.body
            if body:
                body = json.loads(body)
                userName = body['userName']
                if userName == None:
                    return JsonResponse(data = {'status': 400,'success': False, 'message': 'userName not specified in body'}, status = 400)
            else:
                return JsonResponse(data = {'status': 400,'success': False, 'message': 'userName not specified in body'}, status = 400)
            userCheck = userToGroupID(userName)
            if userCheck == None:
                return JsonResponse(data = {"status": 403, 'success': False, 'data': None, 'message': 'User not found'}, status = 403)
            elif userCheck == 'Null':
                return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User not in a group'}, status = 404)
            else:
                users = groupUsers(groupID)
                if users == None:
                    return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'Group not found'}, status = 404)
                elif len(users) == 1:
                    success = deleteGroup(groupID)
                    if success == None:
                        return JsonResponse(data = {"status": 500, 'success': False, 'data': None, 'message': 'Error deleting group'}, status = 500)
                    else:
                        return JsonResponse(data = {"status": 200, 'success': True, 'data': {'group_id': groupID}, 'message': 'Last user from the group removed and group deleted'}, status = 200)
                else:
                    userNum = None
                    for i in range(len(users)):
                        if users[i] == userName:
                            userNum = i+1
                    if userNum == None:
                        return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User not found in group'}, status = 404)
                    else:
                        success = removeUserFromGroup(groupID, userNum)
                        if success == None:
                            return JsonResponse(data = {"status": 500, 'success': False, 'data': None, 'message': 'Error removing user from group'}, status = 500)
                        else:
                            success = removeGroupFromUser(userName)
                            if success == None:
                                return JsonResponse(data = {"status": 500, 'success': False, 'data': None, 'message': 'Error removing group from user'}, status = 500)
                            else:
                                return JsonResponse(data = {"status": 200, 'success': True, 'data': {'group_id': groupID}, 'message': 'User successfully removed from group'}, status = 200)
        else:    
            return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports POST requests.'}, status = 405)
    except Exception as e:
        print(e)
        return JsonResponse(data = {'status': 500,'success': False, 'message': 'Internal Server Error.'}, status = 500)