from django.urls import path

from . import views

urlpatterns = [
    path('<str:userName>/', views.group),
    path('invite/<int:groupID>/', views.groupJoin),
    path('leave/<int:groupID>/', views.groupLeave)
]