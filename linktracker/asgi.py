import os
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linktracker.settings')
django_asgi_app = get_asgi_application()
application = ASGIStaticFilesHandler(django_asgi_app)