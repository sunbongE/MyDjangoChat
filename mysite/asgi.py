"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter  # 이거 추가한거..
from django.core.asgi import get_asgi_application
import app.routing, chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# 요처을 채널스가 먼저 받고
django_asgi_app = get_asgi_application()

# HTTP요청은 장고를 통해 처리하도록 세팅한다.
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            app.routing.websocket_urlpatterns + chat.routing.websocket_urlpatterns
        ),
    }
)
