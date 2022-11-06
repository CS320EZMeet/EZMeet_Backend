from django.db import models
import psycopg2
import env

def userToGroupID(userName):
    groupID = None
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ezmeet-schema\".users WHERE username = %s", (userName,))
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            if(rows):
                i = 0
                for row in rows[0]:
                    if columns[i] == "group_id":
                        if row == None:
                            groupID = 'Null'
                        else:
                            groupID = row
                    i += 1
    return groupID

def groupUsers(groupID):
    users = None
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ezmeet-schema\".group WHERE group_id = %s", (groupID,))
            rows = cursor.fetchall()
            if(rows):
                users = []
                row = rows[0]
                for user in row[1:6]:
                    if user != None:
                        users.append(user)
    return users

def userLocations(users):
    locations = None
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            locations = []
            for user in users:
                cursor.execute("SELECT * FROM \"ezmeet-schema\".user_locations WHERE username = %s", (user,))
                rows = cursor.fetchall()
                if(rows):
                    rows = rows[0]
                    loc = (rows[1], rows[2])
                    locations.append(loc)
    return locations

def createNewGroup(userName):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO \"ezmeet-schema\".group (User1) VALUES (%s) RETURNING group_id;", (userName,))
            rows = cursor.fetchall()
            if(rows):
                groupID = rows[0][0]
        connection.commit()
    return groupID

def updateUserGroup(userName, groupID):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE \"ezmeet-schema\".users SET group_id = {groupID} WHERE username = \'{userName}\' RETURNING group_id;")
            rows = cursor.fetchall()
        connection.commit()
    if len(rows) != 0:
        return 'Success'
    else:
        return None