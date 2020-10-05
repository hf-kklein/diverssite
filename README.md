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

#### apply migrations  

updating master branch to a new version most of the time also requires updating of database structure (i.e. python manage.py migrate). To do so, carry out the following steps

1. open a bash console on your server (This should be available somewhere after login to the server via your browser)
2. activate the virtual environment in the parent directory of .virtualenv directory

  ```bash
  source .virtualenvs/diverssite-virtualenv/bin/activate
  ```
  
3. change database to `saxydivers$default`

  ```bash
  ~/diverssite (master)$ nano .env
  ```

change in there to saxydivers$default and exit and safe file (ctrl+x, then y for saving changes)

4. manually loading environmental vairables is done like this

```bash
set -a; source ~/diverssite/.env; set +a
```

5. apply migrations

```bash
python3 manage.py migrate
```

6. change database in .env back to `saxydivers\$default`

#### WSGI

Our WSGI file in `/var/www/saxydivers_pythonanywhere_com_wsgi.py` looks like this:

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

## Todos
[ ] create superuser: `python manage.py createsuperuser`

[ ] create categs, 'show on pages', and partchoices in admin menu. These are customizeable but some entries are mandatory
because they are referenced in some apps

  + categs (events) `training` `tournament` `social` `other`
  + partchoices (choicetext - choice) `yes - y` `no - n` `maybe - m`
  + show on pages `public` `member`
  + category (wiki) e.g. `Verein`
