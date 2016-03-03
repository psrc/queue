import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainsite.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import django
django.setup()

