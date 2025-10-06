"""
ASGI config for uzuri_university project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzuri_university.settings')

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from my_profile.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzuri_university.settings')

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": AuthMiddlewareStack(
		URLRouter([
			path('ws/notifications/', NotificationConsumer.as_asgi()),
		])
	),
})
