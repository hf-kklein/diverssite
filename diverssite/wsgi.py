# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

## assuming your django settings file is at '/home/saxydivers/mysite/mysite/settings.py'
## and your manage.py is is at '/home/saxydivers/mysite/manage.py'
path = '/home/saxydivers/diverssite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'diverssite.settings'

# load environmental variables
from dotenv import load_dotenv
project_folder = os.path.expanduser('/home/saxydivers/diverssite')
load_dotenv(os.path.join(project_folder, '.env'))

## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
