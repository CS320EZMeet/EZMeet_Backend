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
            i = 0
            for row in cursor.fetchall()[0]:
                if columns[i] == "group_id":
                    if row == None:
                        groupID = 'Null'
                    else:
                        groupID = row
                i += 1
    return groupID

def groupUsers(groupID):
    groupID = 7     #REMEMBER TO REMOVE THE HARDCODE
    users = None
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ezmeet-schema\".group WHERE group_id = %s", (groupID,))
            row = cursor.fetchall()[0]
            users = []
            for user in row[1:6]:
                if user != None:
                    users.append(user)
    return users

def userLocations(users):
    locations = []
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            for user in users:
                cursor.execute("SELECT * FROM \"ezmeet-schema\".user_locations WHERE username = %s", (user,))
                rows = cursor.fetchall()[0]
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
            rows = cursor.fetchall()[0]
            groupID = rows[0]
        connection.commit()
    return groupID

def updateUserGroup(userName, groupID):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE \"ezmeet-schema\".users SET group_id = %d WHERE username = %s RETURNING group_id;", (groupID, userName,))
            rows = cursor.fetchall()[0]
        connection.commit()
    if len(rows) != 0:
        return 'Success'
    else:
        return None