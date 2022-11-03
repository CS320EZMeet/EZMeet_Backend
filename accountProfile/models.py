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