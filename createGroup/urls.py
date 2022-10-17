from django.urls import path
from . import createGroup

#maps views to url

### local:8000/createGroup/
urlpatterns = [
    path('index', createGroup.index)
]