# chat/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('buyer/<int:pk>/', consumers.LiveBiddingConsumer),
]

