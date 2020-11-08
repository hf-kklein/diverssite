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

## Deployment instructions on remote webhosting service

### WSGI webhosting

Our WSGI file in `/var/www/saxydivers_pythonanywhere_com_wsgi.py` looks like this:

```python
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

## assuming your django settings file is at '/home/saxydivers/mysite/mysite/settings.py'
## and your manage.py is is at '/home/saxydivers/mysite/manage.py'
path = '/var/www/files/diverssite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'diverssite.settings'

# load environmental variables
from dotenv import load_dotenv
project_folder = os.path.expanduser(path)
load_dotenv(os.path.join(project_folder, '.env'))

## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Readme for hosting the website on a server  

1. obtain a server and install OS
ideally rent a server from an IaaS platform (e.g. https://www.strato.de/server/linux-vserver/)
If necessary install a current OS on the server (instructions should be available on the hosting website)

2. set up server
follow the instructions on https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04
If you are using a newer OS, there should be a more recent version, but most concepts should be the same

there are possibly some other apps which should be installed.

```bash
sudo apt-get nano  # install text editor for terminal
sudo apt-get install git  # install version control
chsh -s /bin/bash  # to change from dash to bash, in case this is not enabled by default somehow
```

3. set up django app on server
follow instructions on https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04 until activating the virtual environment

if ```source myvenv/bin/activate``` command does not work use ```. myvenv/bin/activate```

you should now have an activated environment shown by (myvenv) $ before the code prompt. Install some packages now

```bash
pip install gunicorn psycopg2-binary
```


4. clone git repository

```bash
git clone https://github.com/flo-schu/diverssite.git
pip install -r requirements.txt
```

5. set up environmental variables

```bash
touch .env
nano .env
```

paste these variables:

export server_ip=REAL_SERVER_IP
export engine=django.db.backends.postgresql_psycopg  # this turns on postgresql engine
export  host=localhost
export db=REAL_DATABASE
export usr=REAL_DATABASE_USER
export pwd=REAL_PASSWORD
export SECRET_KEY=REAL_SECRET_KEY
export DJANGO_DEBUG=False

```bash
echo 'set -a; source ~/sites/diverssite/.env; set +a' >> ~/sites/diverssite/divers_venv/bin/postactivate
set -a; source ~/sites/diverssite/.env; set +a  # try out if .env works
echo $SECRET_KEY
```

6. set up Django app on server

test whether server is running and apply migrations, install fixtures

```bash
python manage.py runserver  # only temporary to debug error messages, break afterwards
python manage.py migrate
python manage.py loaddata fixtures.json  # install fixtures of necessary hardcoded model objects
python manage.py createsuperuser
```

at this point the website should be running without obvious errors

```bash
sudo ufw allow 8000  # adds port 8000 to firewall
python manage.py runserver 0.0.0.0:8000  # test if server runs site
```

7. follow instructions on how to set up gunicorn and nginx.

to reset the server after changes:

```bash
sudo systemctl daemon-reload && sudo systemctl restart gunicorn && sudo systemctl restart nginx
```

8. set up SSL certificate

follow the instructions on https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx
(set up for Ubuntu 18.04 and Nginx)

9. Set up Postfix 
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-on-ubuntu-18-04

when configuring postfix, enter domains
+ saxy-divers.de
+ mail.saxy-divers.de (should be configured at webhoster)
+ sudo apt install policykit-1
+ sudo service postfix reload (after changing main.cf)
+ edit postfix config file if needed:  nano /etc/postfix/main.cf
+ systemctl status postfix.service  # to check status

This should work if all the steps have been carried out correctly



## Maintenance

after changes to the django app have been made:

+ don't push settings from the develop branch
+ ssh onto server
+ navigate into repository
+ activate virtual environment:   source divers_venv/bin/activate
+ pull changes from git repository.
+ activate environmental variables with:   set -a; source ~/sites/diverssite/.env; set +a  
+ migrate changes if necessary:   python3 manage.py migrate
+ restart gunicorn:  sudo systemctl restart gunicorn
+ check if site works. If server error occurs, it could be because changes rely on model values which have not been set. This 
  can be directly tackled in the admin view --> https://mysite.de/admin