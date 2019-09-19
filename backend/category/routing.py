# In routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import *


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path('webssh/', WebSSH),
    ]),

})
