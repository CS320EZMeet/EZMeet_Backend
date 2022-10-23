from django.db import models
import psycopg2

# Create your models here.

def findUser(userName):
    with psycopg2.connect(user="ehrrwfxmrtagrn",
                          password="d82b3292ade726caeb6250c3379b41835b0cd6c78f73e273f865d3f76c0d24f8",
                          host="ec2-54-82-205-3.compute-1.amazonaws.com",
                          port="5432",
                          database="d9ca68j25f19fa") as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM \"ezmeet-schema\".users WHERE name = %s", (userName,))
            columns = [desc[0] for desc in cursor.description]
            real_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return real_dict[0]