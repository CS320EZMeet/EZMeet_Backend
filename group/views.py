from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import userToGroupID, groupUsers, userLocations, createNewGroup, updateUserGroup

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
    if request.method == 'GET':
        groupID = userToGroupID(userName)
        if groupID == 'Null':
            return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User not in a group'}, status = 404)
        elif groupID == None:
            return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User not found'}, status = 404)
        else:
            users = groupUsers(groupID)
            locations = userLocations(users)
            return JsonResponse(data = {"status": 200, 'success': True, 'data': groupDataHelper(groupID, users, locations), 'message': 'Group found'}, status = 200)
    
    elif request.method == 'POST':
        groupID = userToGroupID(userName)
        if groupID == None:
            return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User not found'}, status = 404)
        elif groupID == 'Null':
            groupID = createNewGroup(userName)
            updateUserGroup(userName, groupID)
            return JsonResponse(data = {"status": 200, 'success': True, 'data': {'group_id': groupID}, 'message': 'new group successfully formed'}, status = 200)
        else:
            return JsonResponse(data = {"status": 404, 'success': False, 'data': None, 'message': 'User already in a group'}, status = 404)
    else:    
        return JsonResponse(data = {'status': 405,'success': False, 'message': 'This endpoint only supports GET and POST requests.'}, status = 405)