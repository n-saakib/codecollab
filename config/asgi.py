"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

import projects.routing

# Get the default Django HTTP handler first
django_asgi_app = get_asgi_application()

# This is our main application router
application = ProtocolTypeRouter({
    # For regular HTTP requests, use Django's default handler
    "http": django_asgi_app,

    # For WebSocket connections, use our custom routing
    "websocket": AuthMiddlewareStack(
        URLRouter(
            projects.routing.websocket_urlpatterns
        )
    ),
})
