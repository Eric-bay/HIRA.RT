"""
ASGI config for hira project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import tracker.routing  # Corrected import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hira.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            tracker.routing.websocket_urlpatterns  # Corrected path
        )
    ),
})


