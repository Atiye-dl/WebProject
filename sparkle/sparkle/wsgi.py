"""
WSGI config for sparkle project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
'''
import os

from django.core.wsgi import get_wsgi_application

from accounts.views import create_manager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparkle.settings')

# create user with 'manager' role
create_manager()

application = get_wsgi_application()
'''
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparkle.settings')

application = get_wsgi_application()