# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "diverssite.settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
