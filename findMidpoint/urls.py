from django.urls import path
from . import findMidpoint

#maps views to url

### local:8000/findMidpoint/
urlpatterns = [
    path('index', findMidpoint.index)
]