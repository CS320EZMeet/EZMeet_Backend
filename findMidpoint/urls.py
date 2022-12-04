from django.urls import path
from . import views

#maps views to url

### local:8000/findMidpoint/
urlpatterns = [
    path('', views.index),
    path('<int:groupID>/', views.getMidpoint),
    path('findCommonPreferences/<int:groupID>/', views.findCommonPreferences, name ='commomPref'),
    path('createRecommendation/<int:groupID>/', views.createRecommendationList, name = 'createRec')
]