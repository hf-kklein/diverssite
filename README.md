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
echo "export mysql_db=diverswebsite.db" >> .env
echo "export mysql_usr=saxydivers" >> .env
echo "export mysql_pwd=INSERT_REAL_PASSWORD_HERE" >> .env
echo "export SECRET_KEY=INSERT_REAL_KEY_HERE" >> .env
```
