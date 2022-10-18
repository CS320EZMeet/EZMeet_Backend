from django.urls import path
from . import views

#maps views to url

### local:8000/createGroup/
urlpatterns = [
    path('', views.index)
]