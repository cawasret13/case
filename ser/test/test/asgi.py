"""
ASGI config for test project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import consumersTest, Case, UserWeb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test.settings')
django.setup()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter([
        path('ws/chat/', consumersTest.as_asgi()),
        path('ws/case/', Case.as_asgi()),
        path('ws/user/inventory', UserWeb.as_asgi()),
    ]))
})

