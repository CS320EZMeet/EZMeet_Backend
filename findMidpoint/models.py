from django.db import models
import psycopg2
import env

def getLocation(userName):
    with psycopg2.connect(user=env.USER, 
                          password=env.PASSWORD, 
                          host=env.HOST, 
                          port=env.PORT, 
                          database=env.NAME) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT latitude, longitude FROM \"ezmeet-schema\".user_locations WHERE username = %s", (userName,))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(real_dict) > 1:
        return real_dict
    else:
        return None