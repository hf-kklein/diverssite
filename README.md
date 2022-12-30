# Divers Web Site

Website of Saxy Divers Ultimate Leipzig. Created with Django Web Development
Framework.

## Features

+ add database entries with CSV Files (Events like recurrent trainings, birthdays,
  whatever, user lists, articles, ...), very easy.
+ history of articles and public infos are automatically created and can be
  reverted if mistakes happen. Also abuse can thus be tracked
+ send emails
+ event manager

## install locally for development

0. Prerequisites:
   + install Python
     use python 3.6.9 (this is works for sure) <https://www.python.org/downloads/release/python-369/>
     Make sure to __tick the box "Add to Path"__ or similar. This is important for
     your OS to find the python executable!!!
   + On linux you may need to install pip ```sudo apt install python3-pip```
   + [install git if necessary](https://git-scm.com/downloads))
   + Text editor of your choice (Visual Studio Code, Pycharm, Notepad, Vim, ...) (<https://code.visualstudio.com/>).

1. clone repository into new directory
   ```git clone git@github.com:flo-schu/diverssite.git```

2. ideally with use of command line (cmd, terminal, etc.) navigate inside
   the directory.

3. create a virtual environment (<https://docs.python.org/3/library/venv.html#creating-virtual-environments>)
   inside the project folder (diverssite), in your console type:
   ```python -m venv venv```
   if there are errors, read the error messages and proceed as suggested
   (The specific command may vary depending on your OS (Windows, Linux, Mac))
   this will create a virtual environment called 'venv', which can be understood
   as putting a blank table in your office where you will add all the equipment that
   you need for the project

4. activate the environment (instructions on the same page as above):
   Windows: ```venv\Scripts\activate```
   Linux/Mac: ```source venv\bin\activate```
   To extend the previous analogy. This is like seating yourself at your newly
   placed desk.

5. install requirements (get all the tools for the project, luckily there is a list).
   Pip is the store where you can get all the tools
   update pip: ```python -m pip install --upgrade pip```
   ```pip install -r requirements.txt```

6. create a '.env' file. This files contains all custom settings, which are
   imported when the app is launched. A different version of this is used in
   production (when the site is online), which then contains only absolutely
   secret information. The info in he file used locally are not sensitive and
   therefore can be used without problems. This is why an example file is already
   included:
   __rename the file '.env.example' to '.env'__ (this can be done normally in the
   explorer or with the command line)
   ```cp .env.example .env```

7. The website is now set up. We need to apply some modifications and
   provide fixed datasets to the database for the website to be up and running.
   ````python manage.py migrate``` or ```python3 manage.py migrate```
   Migrations are important for existing databases. The use of __'python3'__ or
   __'python'__ depends on the OS you are using. Use the command that is working
   for the following commands as well.

8. And install fixed data in the database, which the site requires to run:
   ```python manage.py loaddata fixtures.json```

9. That's it. We can test our server. Execute the following and then open your
   browser and go to site: __127.0.0.1:8000__
   ```python manage.py runserver```

10. Create an admin user:
   ```python manage.py createsuperuser```

11. For further infor refer to: <https://docs.djangoproject.com/en/3.1/> and
    <https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website>

## Code Formatting and Conventions

The code is formatted using [black](https://black.readthedocs.io/en/stable/).
The imports are sorted using [isort](https://pycqa.github.io/isort/).
Follow the respective installation instructions. Then run:

```bash
black .
isort .
```

in the repository root directory.

## Hosting the website on a server  

### installation of the basic website

1. obtain a server and install OS
   ideally rent a server from an IaaS platform (e.g. <https://www.strato.de/server/linux-vserver/>)
   If necessary install a current OS on the server (instructions should be available on the hosting website)

2. set up server
   follow the instructions on <https://www.digitalocean.com/community/tutorials/> initial-server-setup-with-ubuntu-18-04
   If you are using a newer OS, there should be a more recent version, but most concepts should be the same

   there are possibly some other apps which should be installed.

   ```bash
   sudo apt-get nano  # install text editor for terminal
   sudo apt-get install git  # install version control
   chsh -s /bin/bash  # to change from dash to bash, in case this is not enabled by default somehow
   ```
  
   register a user on the server which is responsible for ONLY the project
   see: <https://djangodeployment.readthedocs.io/en/latest/03-users-and-directories.html>

3. set up django app on server
   follow instructions on <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04> until activating the virtual environment

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

   paste these variables and replace the values with real stuff. Make sure

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
   export CSRF_COOKIE_SECURE="False"
   export SESSION_COOKIE_SECURE="False"
   ```

   ```set -a; source ~/sites/diverssite/.env; set +a```  # try out if .env works

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
   <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04>

   to get started with nginx, check this guide. It is really helpful 
   to understand what nginx does
   <https://nginx.org/en/docs/beginners_guide.html>

   to reset the server after changes:

   ```bash
   sudo systemctl daemon-reload && sudo systemctl restart gunicorn && sudo systemctl restart nginx
   ```

8. set up SSL certificate

   follow the instructions on <https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx>
   (set up for Ubuntu 18.04 and Nginx)

9. Set up the SMTP Server with Postfix and Dovecot

   What is needed for the whole thing to work is an smtp server with an AUTH function. For this in turn
   I needed an DNS record for the mailserver, but actually everything is described in the next two tutorials. Those are brilliant. Work through them step by step. I added below where I deviated from the instructions
   <https://www.linuxbabe.com/mail-server/setup-basic-postfix-mail-sever-ubuntu>
   <https://www.linuxbabe.com/mail-server/secure-email-server-ubuntu-postfix-dovecot>

   Warning: Here monit is used to automatically restart postfix. Monit caused problems in starting
   postfix. Prefer to not install it

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

## Development

### Migrations

always only migrate the app you have been working on e.g.
```python3 manage.py makemigrations wiki```

for changes that affect a database retrospectively, use of django-extensions `runscript` is recommended

`python3 manage.py runscript save_models`

## Maintenance

### server

#### server restart

+ sudo hostnamectl set-hostname mail.saxy-divers.de (not sure if this is really necessary)
+ sudo systemctl restart gunicorn nginx postfix dovecot

#### after changes to the django app have been made

+ NEVER push settings from the develop branch
+ push if needed changes from main branch
+ ssh onto server  ```ssh username@server```
+ navigate into repository  ```cd xyz```
+ activate virtual environment:   ```source divers_venv/bin/activate```
+ pull changes from git repository.
+ migrate changes if necessary:   ```python3 manage.py migrate```
+ restart gunicorn:  ```sudo systemctl restart gunicorn```
+ check if site works. If server error occurs, it could be because changes rely
  on model values which have not been set. This can be directly tackled in the
  admin view --> <https://mysite.de/admin>
+ restart postfix:  ```sudo systemctl restart postfix```
+ restart dovecot:  ```sudo systemctl restart dovecot```
+ to monitor the status of gunicorn, nginx, dovecot, postfix replace
  ```restart``` with ```status```
+ to create a new mailaccount:
  ```sudo useradd -m username```
  ```sudo passwd username```

### Backup

see <https://django-dbbackup.readthedocs.io/en/master/index.html>

creating backups is done with:

```bash
python3 manage.py dbbackup
python3 manage.py mediabackup
```

for restoring backups see the documentation

### Known Issues and Fixes

#### admin site is not rendered correctly - Sidebar issue

sitebar is triggered out of unknown overflow reasons.
Fix: Disable sidebar
<https://stackoverflow.com/questions/64016816/django-admin-sidebar-bug>

### Roadmap

+ [X] enable email login --> <https://django-allauth.readthedocs.io/en/latest/installation.html>
+ [X] add history and revert possibilities
+ [X] import old email addresses with django-csvimport
+ [X] password reset,
+ [ ] Email activation
+ [ ] update certifcates. Works for mail as well as site, but servers must be restarted
      after the renewal process. This can be automated with certbot.
      Check --deploy-hook for specifics <https://certbot.eff.org/docs/using.html>
+ [X] receive and forward mails (for contact etc.)
+ [X] Make Email Recipients searchable with from
      Lists user firstname, lastname, emailadress
      Groups would be nice (M, F, People registered for event XYZ)
+ [ ] fuzzy search in email search bar (nicht so wichtig)
+ [ ] Events aufhübschen
+ [ ] Feature, mit Email Zustimmung zu xyz abfragen und das zu dokumentieren
+ [ ] Zugang zu contact@saxy-divers.de und ultimail@saxy-divers.de auf webseite
+ [x] fix emails

### Wünsche

+ Mailbenachrichtigung bei neuem turnier
+ kategorien anlegen
