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
            cursor.execute("SELECT Preference_list_id FROM \"ezmeet-schema\".user_preferences WHERE username = %s", (userName,))
            prefID = cursor.fetchone()
    if (len(real_dict) != 0):
        res = real_dict[0]
        res['preferences'] = ["restaurant", "nature", "museums", "entertainment", "shopping"] if prefID is None else generatePreferenceList(prefID[0])
        return res
    else:
        return None

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

def generatePreferenceID(prefList):
    preferences = ["restaurant", "nature", "museums", "entertainment", "shopping"]
    nums = [16, 8, 4, 2, 1]
    res = 0
    for i in range(5):
        if prefList.count(preferences[i]) > 0:
            res += nums[i]

    return res

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
            userName = user['userName']
            for field in ['email', 'password', 'show_location']:
                if user.get(field) is not None:
                    query = f"UPDATE \"ezmeet-schema\".users SET {field} = \'{user[field]}\' WHERE Username = \'{userName}\'"
                    cursor.execute(query)
            if user.get('preferences') is not None:
                id = generatePreferenceID(user['preferences'])
                cursor.execute(f"UPDATE \"ezmeet-schema\".user_preferences SET preference_list_id = {id} WHERE Username = \'{userName}\'")
    return findUser(userName)

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