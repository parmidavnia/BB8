"""
WSGI config for R2D2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
=======
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
>>>>>>> 0cefbfbf6a34f670633a7320b5e7095ca31bc4a0
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R2D2.settings')

application = get_wsgi_application()
