"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

# 웹소켓 처리하는 consumer에서 쿠키/세션/인증을 사용할 수 있다.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator


# 앱에 있는 routing.py를 불러온다.
import app.routing
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(  # AuthMiddlewareStack: 쿠키/세션/인증 사용가능설정.
                URLRouter(  # 불러온 routing.py의 주소들로 접근하면 웹속켓으로 관리한다고 명시한다.
                    app.routing.websocket_urlpatterns
                    + chat.routing.websocket_urlpatterns
                )
            ),
        ),
    }
)
