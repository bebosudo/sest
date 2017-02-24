"""
WSGI config for weather_station_website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

sys.path.append("/home/albertoc/public_html")

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_station_website.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "weather_station_website.settings"

application = get_wsgi_application()
