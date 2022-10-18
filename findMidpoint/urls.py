from django.urls import path
from . import views

#maps views to url

### local:8000/findMidpoint/
urlpatterns = [
    path('', views.index)
]