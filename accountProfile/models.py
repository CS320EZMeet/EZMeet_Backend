from django.db import models
import psycopg2
import env

# 'User' object is defined to contain all of a user's parameters in the User table of DB, plus their preference list

# Find user with given userName in DB. Return their User object if they exist, else None
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
            cursor.execute("SELECT Preference_list_id FROM \"ezmeet-schema\".user_preferences WHERE username = %s", (userName,))
            prefID = cursor.fetchone()
            if (len(real_dict) != 0):
                res = real_dict[0]
                if prefID is None:
                    res['preferences'] = ["restaurant", "nature", "museums", "entertainment", "shopping"]
                    query = f"INSERT INTO \"ezmeet-schema\".user_preferences (Username, Preference_list_id) VALUES (\'{userName}\', 31)"
                    cursor.execute(query)
                else:
                    res['preferences'] = generatePreferenceList(prefID[0])
                return res
            else:
                return None

# Helper to convert Preference ID from DB to Preference List
def generatePreferenceList(prefID):
    preferences = ["restaurant", "nature", "museums", "entertainment", "shopping"]
    res = []
    pow = 16
    for i in range(5):
        if prefID >= pow:
            res.append(preferences[i])
            prefID -= pow
        pow /= 2

    return res

# Helper to convert Preference List from front-end to Preference ID
def generatePreferenceID(prefList):
    preferences = ["restaurant", "nature", "museums", "entertainment", "shopping"]
    nums = [16, 8, 4, 2, 1]
    res = 0
    for i in range(5):
        if prefList.count(preferences[i]) > 0:
            res += nums[i]

    return res

# Given essential User parameters (Username, Email, Password), add User to DB
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

# Given any subset of a User object that includes a userName, update altered fields corresponding to that userName in DB
def updateFields(user):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            userName = user['userName']
            for field in ['email', 'password', 'show_location']:
                if user.get(field) is not None:
                    query = f"UPDATE \"ezmeet-schema\".users SET {field} = \'{user[field]}\' WHERE Username = \'{userName}\'"
                    cursor.execute(query)
            if user.get('preferences') is not None:
                id = generatePreferenceID(user['preferences'])
                cursor.execute(f"UPDATE \"ezmeet-schema\".user_preferences SET preference_list_id = {id} WHERE Username = \'{userName}\'")
    return findUser(userName)

# Given a userName, fetch the location of that user from DB
def findLocation(userName):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT latitude, longitude, address FROM \"ezmeet-schema\".user_locations WHERE Username = %s", (userName,))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(real_dict) != 0:
        return real_dict[0]
    else:
        return None

# Given a user's userName, and a new latitude, longitude, and address string, update that user's location correspondingly
def updateLocation(userName, latitude, longitude, address):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE \"ezmeet-schema\".user_locations SET latitude = {latitude}, longitude = {longitude}, address = \'{address}\' WHERE Username = \'{userName}\'")
            rowCount = cursor.rowcount
    if rowCount != 0:
        return 'Success'
    else:
        return None