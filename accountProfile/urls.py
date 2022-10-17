from django.urls import path
from . import accountProfile

#maps views to url

### local:8000/accountProfile/
urlpatterns = [
    path('index', accountProfile.index)
]