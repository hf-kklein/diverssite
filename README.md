# Divers Web Site
Website of Saxy Divers Ultimate Leipzig.
## Deployment Instructions for Python Anywhere
### Create a MySQL Database
Therefore open the database tab and create a new database. Remember the name and credentials for later.
### Follow the official Python Anyhwere Docs
 + [Running an existing Django Project](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject)
 + [Setting Environment Variables](https://help.pythonanywhere.com/pages/environment-variables-for-web-apps)

The mandatory environment variables are:
+ `SECRET_KEY` (this is the django secret key)
+ `mysql_host`
+ `mysql_db`
+ `mysql_usr`
+ `mysql_pwd`
+ `mysql_port`

Here's a template to set them:
```bash
echo "export mysql_host=saxydivers.mysql.pythonanywhere-services.com" >> .env
echo "export mysql_db=saxydivers\$default" >> .env
echo "export mysql_usr=saxydivers" >> .env
echo "export mysql_pwd=INSERT_REAL_PASSWORD_HERE" >> .env
echo "export SECRET_KEY=INSERT_REAL_KEY_HERE" >> .env
```
using an other database than `saxydivers$default` results in an error during login when running the migrations.

### Our WSGI file looks like this:
```python
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

```
