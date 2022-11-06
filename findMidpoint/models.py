from django.db import models
import psycopg2
import env

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