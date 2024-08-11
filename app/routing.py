from django.urls import path
from .consumers import NormalConsumer

websocket_urlpatterns = [
    path('ws/<str:room_name>/',NormalConsumer.as_asgi()),
    ]