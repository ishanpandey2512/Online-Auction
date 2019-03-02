# chat/routing.py
from django.conf.urls import url, re_path
from . import consumers

websocket_urlpatterns = [
    url(r'^app/buyer/(?P<p_id>[0-9]+)/$', consumers.LiveBiddingConsumer),
]

