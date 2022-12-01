from django.db import models
import psycopg2
import env

def findUser(userName):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ezmeet-schema\".users WHERE username = %s", (userName,))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(real_dict) != 0:
        return real_dict[0]
    else:
        return None

def createUser(user):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO \"ezmeet-schema\".users (Username, Password, Email) VALUES (%s, %s, %s)",
                           (user['userName'], user['password'], user['email']))
    return user

def updateFields(user):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            userName = user.userName
            for field in user.keys():
                cursor.execute("UPDATE \"ezmeet-schema\".users %s = %s WHERE Username = %s", (field, user['field'], userName))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(real_dict) != 0:
        return real_dict[0]
    else:
        return None

def findLocation(userName):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT latitude, longitude FROM \"ezmeet-schema\".user_locations WHERE Username = %s", (userName,))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(real_dict) != 0:
        return real_dict[0]
    else:
        return None

def updateLocation(userName, latitude, longitude):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE \"ezmeet-schema\".user_locations SET latitude = %s, longitude = %s WHERE Username = %s", (latitude, longitude, userName))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(real_dict) != 0:
        return real_dict[0]
    else:
        return None