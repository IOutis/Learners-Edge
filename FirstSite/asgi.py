"""
ASGI config for FirstSite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter,URLResolver,URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FirstSite.settings')


django.setup()
from channels.auth import AuthMiddleware, AuthMiddlewareStack
from notifications_app.routing import websocket_urlpatterns
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
    })