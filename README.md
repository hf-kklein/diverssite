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

2.1 register a user on the server which is responsible for ONLY the project
see: https://djangodeployment.readthedocs.io/en/latest/03-users-and-directories.html

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

```bash
export server_ip=REAL_SERVER_IP
export engine=django.db.backends.postgresql_psycopg  # this turns on postgresql engine
export host=localhost
export db=REAL_DATABASE
export usr=REAL_DATABASE_USER
export pwd=REAL_PASSWORD
export SECRET_KEY=REAL_SECRET_KEY
export DJANGO_DEBUG=False
export SSL_REDIRECT=True
```

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
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

to reset the server after changes:

```bash
sudo systemctl daemon-reload && sudo systemctl restart gunicorn && sudo systemctl restart nginx
```

7. 2 when everythin has been installed, me move all installation files into 
a system directory as root user and create a systemuser to execute the files:

+ first log into root by typing :  ```su```

+ copy files ($USER) is the name of the user under which everything was done so far

```bash
cp -r /home/$USER/sites/diverssite/ /opt/diverssite
```

+ reinstall virtualenv

```bash
rm -r /opt/diverssite/divers_venv
virtualenv --system-site-packages --python=/usr/bin/python3 /opt/diverssite/venv
/opt/diverssite/venv/bin/pip install -r /opt/diverssite/requirements.txt
```

+ pre compile python files because they cannot be accessed by systemuser

```bash
/opt/diverssite/venv/bin/python -m compileall -x /opt/divessite/venv/ /opt/diverssite
```

+ create a system user

```bash
adduser --system --home=/var/opt/diverssite \
    --no-create-home --disabled-password --group \
    --shell=/bin/bash saxydivers
```

+ create data directory for files which is different from the program directory

```bash
mkdir -p /var/opt/diverssite
chown saxydivers /var/opt/diverssite

mkdir -p /var/log/diverssite
chown saxydivers /var/log/diverssite
```

+ make contents of production settings (/etc/opt/diverssite) unreadable to others

```bash
chgrp saxydivers /etc/opt/diverssite
chmod u=rwx,g=rx,o= /etc/opt/diverssite
```

+ test django server

```bash
su saxydivers
source /opt/diverssite/venv/bin/activate
set -a; source /opt/diverssite/.env; set +a
python /opt/diverssite/manage.py runserver 0.0.0.0:8000
```

development server can now be accessed via http://saxy-divers.de:8000

+ todo: 
++ give florian permission on opt/diverssite and var/opt/diverssite

8. set up SSL certificate

follow the instructions on https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx
(set up for Ubuntu 18.04 and Nginx)

9. Set up the SMTP Server with Postfix and Dovecot

What is needed for the whole thing to work is an smtp server with an AUTH function. For this in turn
I needed an DNS record for the mailserver, but actually everything is described in the next two tutorials. Those are brilliant. Work through them step by step. I added below where I deviated from the instructions
https://www.linuxbabe.com/mail-server/setup-basic-postfix-mail-sever-ubuntu
https://www.linuxbabe.com/mail-server/secure-email-server-ubuntu-postfix-dovecot

+ set hostname: This may actually be not required because later on we fix the hostname in postfix config
```sudo hostnamectl set-hostname mail.saxy-divers.de```
+ follow the rest of the tutorial

+ open the aliases file
```sudo nano /etc/aliases```

+ add the line to aliases file, so that error mails are sent to an external mail in case the server breaks down
```root:          your@mail.de```

+ updating certificate to email instead of creating a new one:
```certbot --expand -d saxy-divers.de,mail.saxy-divers.de```

+ dont use the auth_username_format = %n option. I think it will be simpler to just use usernames.
+ enabling monit at the end of part 1 tutorial caused problems. Disabling it fixed postifx shutting down repeatedly

To check problems of postifx and dovecot inspect the log

+ check mailbox:
```nano /var/mail/florian```
+ check log:
```nano /var/log/mail.log```

+ then add the environmental variables to the settings file and add them to the .env file on the server like under point 3. email_usr and email_pw müssen gesetzt sein. Dafür muss auf dem SMTP Server ein benutzer existieren. Dies sollte aber schon im Tutorial geschehen sein.

```bash
export email_tls=True
export email_default_from=ultimail@saxy-divers.de
export email_host=mail.saxy-divers.de
export email_usr=XXXXXX
export email_pw=XXXXXX
export email_port=587
```

## Maintenance

after changes to the django app have been made:

+ NEVER push settings from the develop branch
+ push if needed changes from main branch
+ ssh onto server  ```ssh username@server```
+ navigate into repository  ```cd xyz```
+ activate virtual environment:   ```source divers_venv/bin/activate```
+ pull changes from git repository.
+ activate environmental variables with:   ```set -a; source ~/sites/diverssite/.env; set +a```  
+ migrate changes if necessary:   ```python3 manage.py migrate```
+ restart gunicorn:  ```sudo systemctl restart gunicorn```
+ check if site works. If server error occurs, it could be because changes rely on model values which have not been set. This can be directly tackled in the admin view --> https://mysite.de/admin
+ restart postfix:  ```sudo systemctl restart postfix```
+ restart dovecot:  ```sudo systemctl restart dovecot```
+ to monitor the status of gunicorn, nginx, dovecot, postfix replace ```restart``` with ```status```