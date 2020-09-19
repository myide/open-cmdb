# In routing.py
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.urls import path

from category.ssh.webssh_consumers import WebSSH

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path('webssh/', WebSSH),
    ]),

})
