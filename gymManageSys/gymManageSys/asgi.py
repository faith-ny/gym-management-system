"""
ASGI config for gymManageSys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymManageSys.settings')
from channels.routing import ProtocolTypeRouter, URLRouter

import main.routing

#application = get_asgi_application()
application=ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': URLRouter(main.routing.ws_patterns)
})
