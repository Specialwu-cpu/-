"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from django_project import urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')


application = get_asgi_application()

# application = ProtocolTypeRouter(
#     # 'django_project.asgi.application'
#     # {
#     #     "http": get_asgi_application(),
#     #     "websocket": AuthMiddlewareStack(
#     #         URLRouter(
#     #             urls.websocket_urlpatterns
#     #         )
#     #     ),
#     # }
# )
