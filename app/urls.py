from django.urls import path
from .views import *
urlpatterns = [
    path('signin/',signin,name="signin"),
    path('signup/',signup,name="signup"),
    path('logout/',logout,name="logout"),
    path('',home,name="rooms"),
    path('room/<slug:slug>/',room,name="room"),
    path('create/',create_room,name="createroom"),
    path("room/enter/<str:id>",enter,name="enter"),
    path('delete/<str:id>',delete_room,name='delete'),
    path('change/<str:id>',change_password,name="change"),

]