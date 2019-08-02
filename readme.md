[![Build Status](https://scrutinizer-ci.com/g/PHPirates/django-template/badges/build.png?b=master)](https://scrutinizer-ci.com/g/PHPirates/django-template/build-status/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/PHPirates/django-template/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/PHPirates/django-template/?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1e52d96b4c3b4bc586827a483287ec3c)](https://www.codacy.com/app/PHPirates/django-template?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=PHPirates/django-template&amp;utm_campaign=Badge_Grade)
[![Codeclimate](https://api.codeclimate.com/v1/badges/7ee6b92b294863348693/maintainability)](https://codeclimate.com/github/PHPirates/django-template/maintainability)

# Django template project and deployment tutorial

### Makes use of

#### For the website:
* PostgreSQL
* The [TinyMCE](https://www.tinymce.com/) editor
* HTML templates
* CSS
* Directory structure from [docs.djangoproject.com](https://docs.djangoproject.com/en/1.11/intro/tutorial01/).

#### For deployment:
* A PostgreSQL database
* gunicorn to serve the website
* nginx to 'reverse proxy' requests from outside to gunicorn
* PyCharm for local and remote development
* supervisor to manage gunicorn

This guide has been tested a lot of times on Ubuntu 16.04, 18.04, Raspbian Buster and even Arch Linux.

## Table of Contents
- [Instructions to run the website locally](#instructions-to-run-the-website-locally)
  * [Setting up postgres locally](#setting-up-postgres-locally)
- [Deploying on an Ubuntu server](#deploying-on-an-ubuntu-server)
  * [Buy the necessary services](#buy-the-necessary-services)
  * [Setting up users and login](#setting-up-users-and-login)
  * [Firewall and fail2ban](#firewall-and-fail2ban)
  * [Local setup](#local-setup)
  * [Setting up postgres](#postgres)
  * [Setting up a virtual environment](#setting-up-a-virtual-environment)
  * [Uploading project](#uploading-project)
  * [Installing dependencies](#installing-dependencies)
  * [Setting up gunicorn](#setting-up-gunicorn)
  * [Setting up supervisor](#setting-up-supervisor)
  * [Setting up nginx](#setting-up-nginx)
  * [Setting up HTTPS](#setting-up-https)
  * [Start nginx](#start-nginx)
    + [Setting up automatic renewal of https certificates](#setting-up-automatic-renewal-of-https-certificates)
  * [<a name="remember">To remember</a>](#-a-name--remember--to-remember--a-)
    + [Django files](#django-files)
    + [Django models](#django-models)
    + [Static files](#static-files)
    + [Supervisor config](#supervisor-config)
    + [gunicorn start script](#gunicorn-start-script)
    + [nginx config](#nginx-config)
    + [logs](#logs)


# Instructions to run the website locally

1. Create a project either by creating a new Django project in PyCharm and then copying the files from this project or by downloading this template project directly.
1. Probably you want to use a virtual environment.
1. Check that the packages in requirements.txt are installed, on Windows you may need to download the `mysqlclient` package from [lfd.uci.edu](http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python) selecting the right bits version for you python (you can check that by starting ``python``), copy it to the project location, check there with `pip -V` that you are using the pip of the virtual environment and then run `pip install mysqlclient-1.3.13-cp37-cp37m-win32.whl`. On Linux you can download a `mysqlclient` package from your distro's package repo, you also need `gcc`.
1. If you use PyCharm, you can make a Django Server run configuration (instead of running `runserver` all the time). Add an environment variable with name `DJANGO_SETTINGS_MODULE` and value `mysite.settings.development`, assuming the settings are in `development.py` in a folder `settings` in the folder `mysite`. The development settings are for development on your local computer, production settings are for production on the server.
1. Tip: If you try running with `DEBUG=False` on your local computer, Django won't serve your static files for you since this is only meant for in production.
1. Possibly you need to select your Python interpreter.

#### Setting up postgres locally
1. To use a database locally, do the following. On Linux you can also not use pgAdmin but do everything via the command line, just continue to set up postgres like below and then go the instructions linked there.
   1. Install PostgreSQL (go to the website on Windows, use your package manager on Linux) 
   1. Install pgAdmin (these instructions were tested on Windows with pgAdmin 4 2.0 and on Arch Linux with pgAdmin 4 4.1) or use the command prompt PostgreSQL tools for the next steps
   1. On Windows:
       1. To create a user, right-click on PostgreSQL and choose create Login/Group Role, give it for example the name of your project.
       1. Create a database by right-clicking on Databases, give it a name for example myproject_db, and under the 'security' tab grant all privileges to the user you just created.
   1. On Linux (tested on Arch Linux, on other distros commands may differ)
        1. Switch to the postgres user with `sudo su postgres`
        1. Initialize postgres with `initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'`
        1. Switch back to your own user (or open a new terminal window)
        1. Start the postgresql service with `sudo systemctl start postgresql` and `sudo systemctl enable postgresql`
        1. Change to a directory which `psql` can access, like `cd /tmp`
        1. Either use pgAdmin, or reuse the way of working from the server: do the first part of the [postgres section](#postgres) below (until you exit psql) now. If you use pgAdmin:
        1. Create a server with a name like `mysite_server` and host name `127.0.0.1` and user postgres, empty password.
       1. Right click on Login/Group Roles and Create a Role, name it something like `mysite_user` and under Privileges give it the login privilege.
       1. If you get the error `'psycopg2.extensions.Column' object has no attribute '_asdict'` then you have a version mismatch between psycopg2 and pgAdmin, probably psycopg2 is newer than your pgAdmin version (e.g. pgAdmin4 4.4 and psycopg2 2.8.2 will not work). Try updating everything (for newer pgAdmin version you can search online) and if it doesn't help use the command line (link above) to continue.
       1. Create a database by right-clicking on Databases, give it a name for example myproject_db, select as owner mysite_user and under the 'security' tab add a privilege with grantee mysite_user, grant all privileges to the user you just created.
   1. Replace name, user and password in `DATABASES` in your settings file.
   
1. Use edit | find | replace in path to replace all references to 'mysite' to our own project name. Also rename the 'mysite' module (take care to be consistent with capitalization).
1. (Professional edition of PyCharm only) To run `manage.py` tasks, go to settings | Languages and Frameworks | Django and specify your settings file (in this case development, which includes base). Then you can use Tools | Run manage.py Task (`CTRL` + `ALT` + `R`) to run tasks like `migrate`.
1. Each time after you made changes in your models in models.py, run `makemigrations` and `migrate` to apply the changes to the database. Do that now.
1. Also as `manage.py` task, run `createsuperuser --username myname` to create a superuser (for example you) for your website backend.
1. Use the run configuration you made or run `runserver`.
1. Access the backend by navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

(tip) If you already have a local website running, changing the port number allows you to keep things separate.

# Deploying on an Ubuntu server
There are a lot of tutorials around, but I have noticed that instructions get obsolete very quickly, so preferably select the latest one you can find which uses exactly all the tools you want. For me that was the one I had to write myself, as below.

We will use a **postgres** database, **gunicorn** to serve the website, and **nginx** to 'reverse proxy' requests from outside to gunicorn.
It makes life easier if you also use **PyCharm**, and **supervisor** to manage gunicorn.

## Buy the necessary services

1. You will want to buy a VPS, which is a (virtual) server on which you can install whatever you want. Make sure not to buy something called 'shared hosting' as it probably means you can only upload static files. At the moment a VPS can be as cheap as five euros a month.
1. If, when buying a VPS, you can choose between a pre-installed or ISO-VPS, choose the ISO-VPS, i.e. choose the option with the most freedom (avoid 'time-saving' options).
1. For this tutorial we will assume you have chosen the latest Ubuntu version, this tutorial is tested with Ubuntu 16.04 and 18.04.
1. If you don't have a domain yet, you can probably buy it via the same company as you bought the VPS. If you have one, you can probably transfer the management of it to that company. You could also leave it as you have it, and just point the DNS to the ip address of the VPS.

From now on we assume that the server is already up and running and that you can execute `sudo` commands via SSH, for example using `ssh root@xxx.xxx.xxx.xxx` in bash.
If not, for example because you have walked through the Ubuntu installation yourself, make sure you install `openssh-server` (with `sudo apt install openssh-server`).
If you cannot access because you have no root password, you should have created an other user, say `eve`.
Then you should be able to login with `eve` instead of `root`.

Run `sudo apt update` and `sudo apt upgrade` before anything.
Random remark: note that `apt` is the user command, `apt-get` is the low-level command useful for scripting.

## Setting up users and login

1. If you already have a second user besides root, skip this step. Otherwise, log in via SSH with the root user. Create a new user with your name with `adduser eve`. Give her root permissions with `usermod -aG sudo eve`. Impersonate her with `sudo su - eve`. Note you have to do this and the next three instructions (adding a public key) for every user you want to give access to the server.
1. Set up login with a key pair, if needed on your local computer generate keys with `ssh-keygen -t rsa`, otherwise reuse the key you have. View your public key by executing (locally) in bash `cat ~/.ssh/id_rsa.pub` and copy *all* of the output. 
1. To put it on the server, use `mkdir ~/.ssh` to create the directory, `chmod 700 ~/.ssh` to change permissions, `nano ~/.ssh/authorized_keys` (nano is a text editor, you can also use vim) to put the key in this file and `chmod 600 ~/.ssh/authorized_keys`.
1. Test that it works by opening a new bash window and check that you can login with eve without needing to enter your password.

## Firewall and fail2ban
1. Install a firewall, `sudo apt install ufw`.
1. Allow SSH (22), Postgres (5432), http (80) and https (443) and other things you can think of: `sudo ufw allow xxx` where `xxx` is a port number.
1. `sudo ufw enable` and check with `sudo ufw status`.
1. Before closing your existing connection to the server, check if you can login to a new session! Otherwise you could lock yourself out.
1. Besides a firewall, you also want to protect your server against bots that repeatedly try to guess your password, for that you can install `sudo apt install -y fail2ban`.
1. Create a new file `sudo nano /etc/fail2ban/jail.local` and put into it
```
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
```
1. Start and enable (start on boot) the service with `sudo systemctl start fail2ban` and `sudo systemctl enable fail2ban`.

## Local setup
1. Add your server to PyCharm in Settings | Build, Execution, Deployment | Deployment, click on the plus icon, choose SFTP, enter the IP address of your server in SFTP host, specify user name, choose as authentication Key Pair and specify your key file, for Windows probably in `C:\Users\username\.ssh\id_rsa` or on Linux `/home/username/.ssh/id_rsa`. Also, if not already done, specify web server url as `http://myipadress`. 
    1. If you get the error 'Keypair is corrupt or has unknown format', then try selecting OpenSSH config as Authentication instead.
    1. If you then still cannot make a connection, use password authentication.
1. Make the server the default one by clicking an icon a few to the right of the 'plus' you used to add the server. When the server name becomes bold, you have set it as default.
1. Go to Settings | Tools | SSH Terminal and select the server as Deployment server.
1. You should now be able to ssh into your server with Tools | Start SSH Session (assigning a shortcut to this is a good idea: go to Settings | Keymap, search for 'start ssh' and add a shortcut, e.g. <kbd>Alt</kbd>+<kbd>S</kbd>).

1. If needed (and if you already want your website domain to point to this VPS) point your (sub)domain to the ip address of your server, probably in the settings of the provider where you registered the domains. This can take a few hours to take effect.

1. Install the packages we need with `sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx`.

## <a name="postgres">Setting up postgres</a>
1. Start a postgres session with `sudo -u postgres psql`.
1. `CREATE DATABASE mysite_db;`
1. `CREATE USER mysite WITH PASSWORD '1234';`
1. `ALTER ROLE mysite SET client_encoding TO 'utf8';`
1. `ALTER ROLE mysite SET default_transaction_isolation TO 'read committed';`
1. Now check if the timezone in `settings/base.py` is correct, if not you can modify it to for example `Europe/Amsterdam`. Then `ALTER ROLE mysite SET timezone TO 'Europe/Amsterdam';`
1. `GRANT ALL PRIVILEGES ON DATABASE mysite_db TO mysite;`
1. If you want to use tests which use the database (recommended, see https://docs.djangoproject.com/en/2.2/topics/testing/overview/) you also need to run `ALTER USER mysite CREATEDB;`
1. `\q` to exit
1. Update the production database settings in `mysite/settings/production.py`
1. Generate a new secret key to enter in the same file. For example using PyCharm's Python console with
```python
from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^*(-_=+)'
print(get_random_string(50, chars))
```
1. Make sure to keep this file secret. Also don't forget to check `DEBUG = False` in here.
1. While you're there, also add your website domain to `ALLOWED_HOSTS` in the base settings. Be sure to add your server's ip address as well if you want to debug with that!
1. Lastly, to enable connection from outside, you need to add to `/etc/postgresql/9.5/main/postgresql.conf` just at the end, `listen_addresses = '*'` and in `/etc/postgresl/9.5/main/pg_hba.conf` you need to add `host all all 0.0.0.0/0 md5`.
1. Restart postgres with `sudo /etc/init.d/postgresql restart`.
1. If at any time you get the error 
```
psycopg2.OperationalError: could not connect to server: Connection refused
	Is the server running on host "x.x.x.x" and accepting
	TCP/IP connections on port 5432?
```
then the previous steps could be the problem (or your firewall is still blocking 5432, of course, or ... ).


## Setting up a virtual environment
1. Check that you're running the python 3 version of pip with `pip -V`. If not, try `pip3 -V`. If that works, you have to substitute `pip` with `pip3` from now on.
1. Similarly, check if you're using python 3 with `python -V`, and if you need `python3` then substitute, or do something else to fix it.
    * If you need Python 3.7 but the Linux distribution you have doesn't have it, you can follow instructions at https://serverfault.com/a/919064/437404 because this will also install pip. Now you will need to use `python3.7` and `pip3.7` instead of `python` and `pip` in any command. Do not remove the default installed python 3.5.
1. Install the package with `pip install virtualenv`.
    * If this fails because of permissions, ensure ownership of python to install packages with `sudo chown -R eve:eve /usr/local`.
1. I happen to want my virtual environments in `/opt/` so I do `cd /opt`.
    * (if you are the only person who is ever going to work on it, putting it in `/home/username` would avoid some permission problems)
1. Make sure you create a virtual environment with the latest python you installed! Creating a virtual environment appears to be very much liable to change with python versions, so if the following steps don't work just search for instructions for your specific environment.
1. Install venv with `sudo apt install python3-venv`.
1. I had python 3.5 installed, checked with `python3.5 -V`. Then you should be able to create a virtual environment with `sudo python3.5 -m venv mysite_env`. Same for 3.7 etc.
    * If that does not work, I once solved that under python 3.6 by doing `sudo python3.6 -m venv --without-pip mysite_env`, `source mysite_env/bin/activate`, `sudo apt install curl`, then found out curl doesn't run as sudo so did `sudo bash -c "curl https://bootstrap.pypa.io/get-pip.py | python"` then `deactivate`. 
1. Every time you want to do something in your virtual environment, activate it with (change `mysite` to your website name) `source mysite_env/bin/activate`. Do so, now.
1. Check with `python -V` for correct python version, and `pip -V` for correct pip version in the correct location (should be in the virtual environment).
    * If you did set the virtual environment up without pip, download it with `wget https://bootstrap.pypa.io/get-pip.py`, install with `python3.6 get-pip.py`. 
1. Check with `which pip` and `which python` that everything points inside your virtual environment. If you do need to use for example `python3.6` instead of `python`, remember that or fix the `python` command to avoid mistakes.

## Uploading project
1. `cd mysite_env` and `sudo mkdir mysite`, then correct ownership with `sudo chown -R eve:eve /opt/`.
1. In PyCharm, go to the deployment settings of your server as before and edit Root path to the directory you just created, so `/opt/mysite_env/mysite`. Under Mappings, specify `/` as Deployment Path. 
1. Under Options (click on the arrow next to Deployment in the left menu) you can specify to upload changes automatically or if you hit `CTRL+S`. Click Ok.
1. You don't want to upload everything you have locally to the server, for example it makes no sense to upload files in your local virtual environment. To exclude these paths, go to Settings | Build, Execution, Deployment | Deployment | Excluded Paths and add them, by hitting the plus icon and choosing Local Path.
    * You may notice that if you try to exclude a folder which is marked as Excluded in PyCharm (not excluded from upload, but excluded like not belonging to the project, which you can see as the folder is marked red) then you cannot exclude it from deployment and you will get a message saying 'Local path is out of project'. (Note, however, that sometimes you *can* exclude it even though you get the warning.) This is a bug in PyCharm, vote for it at https://youtrack.jetbrains.com/issue/WI-7367. To exclude these folders for deployment, first unmark them as excluded by right-clicking on them and choosing Mark Directory as | Cancel Exclusion. Now you can exclude them for deployment, and mark them again as excluded after you did that (PyCharm will give an error in the settings but it will still work).
1. Now theoretically you should be able to upload everything by hitting <kbd>Ctrl</kbd>+<kbd>S</kbd>, but we have found that often this does not work. A more reliable way is to first select your project folder in the project view on the left (probably the topmost folder) and selecting Tools | Deployment | Upload to ..., or using the default shortcut <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> and choosing your server.

## Installing dependencies
1. If you need `msqlclient`, first install `sudo apt install python3.5-dev libmysqlclient-dev` which are needed for the `mysqlclient` package.
1. If you didn't remember, check with `which python` (with virtualenv activated) where your python hides, then in PyCharm go to Settings | Project ... | Project Interpreter and add a new remote one by selecting the gear icon at the top right.
1. Select SSH Interpreter in the left menu, then Existing Server Configuration, select as Deployment Configuration your server and Move Deployment Server, then select the right path to your python _of the virtual environment_. Also take care to change the Sync paths, of which the remote path probably should be `/` - but make sure to check the Deployment path under Mappings afterwards and reset it to `/`.
1. PyCharm should warn you about some dependencies from requirements.txt not being installed, do that. Probably PyCharm will also install helper files which can take a long time.
1. Make sure you have the remote python selected as interpreter, (you can also check for package updates there), now you can just like before hit Tools | Run Manage.py Task and run `makemigrations` and `migrate` but now both with production settings: so `makemigrations --settings=mysite.settings.production` and also for `migrate`.
1. If that fails, try running these tasks manually, so go to `/opt/mysite_env/mysite` and run `python manage.py makemigrations` and same for `migrate`.
1. If needed, create superuser just as with local setup, `createsuperuser --username myname`.
1. Run the manage.py task `collectstatic --settings=mysite.settings.production` to gather static files for nginx to serve.
1. Double-check that Deployment Settings | Mappings | Deployment Path is set to `/`, PyCharm sometimes resets this. If this is wrong, uploading files won't work properly. 

## Setting up gunicorn
1. We will setup gunicorn such that nginx will be able to redirect requests to gunicorn which is bound to the Django server.
1. Copy the contents of the [`gunicorn_start`](server%20configuration%20files/gunicorn_start) script in `/opt/mysite_env/bin/` (after changing all the paths, of course), create file with `nano /opt/mysite_env/bin/gunicorn_start` (do not use sudo or FileZilla here) and make sure it has executable permissions with `sudo chmod u+x /opt/mysite_env/bin/gunicorn_start`.

## Setting up supervisor
1. We use supervisor to manage the starting and stopping of gunicorn. If your server would crash or for whatever reason is restarted, this makes sure to automatically start your website too.
1. Install with `sudo apt install supervisor`.
1. Put the file [`mysite.conf`](server%20configuration%20files/mysite.conf) in `sudo nano /etc/supervisor/conf.d/mysite.conf`, make sure it has executable permissions just like with the gunicorn start script.
1. Every time after you change such a supervisor config file, you have to do `sudo supervisorctl reread` and `sudo supervisorctl update`. Do this now. I gathered things to remember like this [below](#remember).
1. You can manually restart with `sudo supervisorctl restart mysite`.

## Setting up nginx
1. Install with `sudo apt install nginx`
1. If you do not have the folders `/etc/nginx/sites-available/` and `/etc/nginx/sites-enabled`, you can create them and you also need to include them by putting in `/etc/nginx/nginx.conf` at the bottom of the `http` block the following:
```
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
```
and remove the `server` block in the `http` block.
1. Edit the content of the  [`nginx-config`](server%20configuration%20files/nginx-config) into the file `sudo nano /etc/nginx/sites-available/mysite`. We will set up https later.
1. Enable your site by making the symbolic link `sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/mysite`
1. Remove the symbolic link to the default config, `sudo rm /etc/nginx/sites-available/default` and `sudo rm /etc/nginx/sites-enabled/default`
1. Create empty log file `mkdir /opt/mysite_env/mysite/logs/` and `touch /opt/mysite_env/mysite/logs/nginx-access.log`.
1. Make the socket directory with `mkdir /opt/mysite_env/mysite/run/`.
1. Create an empty socket file `touch /opt/mysite_env/mysite/run/gunicorn.sock` in the same way, and also `sudo chmod 666 /opt/mysite_env/mysite/run/gunicorn.sock`. If at any time you get the error that this is not a socket, remove it. A socket is just a text file, with the great usefulness of enabling nginx to talk to gunicorn in a language that they both understand.
1. Make sure the lines in the nginx config which point to the ssl certificates are commented.
1. Test the syntax of your nginx config file with `sudo nginx -t` and fix any.

1. Make sure you have your ip and domain (without the `http(s)://` prefix, but both with and without the `www.` prefix) in allowed hosts in your Django settings file.
1. If you will set up https later, you can skip the https section below, but make sure to start nginx in the section after that.

## Setting up HTTPS
Because it's not much work and free, just do it. You need to have your domain pointing to your ip address already.

1. You can get an ssl certificate for free, for example from Let's Encrypt. In that case, just follow their [install guide](https://certbot.eff.org/#ubuntuxenial-nginx). 
1. When running certbot, when it asks for domains provide it both with and without the `www.` prefix. If you need to choose, you are not serving files out of a directory on the server. 
1. Either choose in the certbot setup to redirect http to https (in which case you need to add your domain without `www.` prefix to `server_name` in the largest `server ` block) or do this yourself by uncommenting the https-related parts in the `nginx-config`, marked with `# ---- HTTPS setup start/end ----`, and remove the `listen 80;` line.
1. In any case, make sure the main server block has only one `listen ...` line, one `server_name ...` line etc.
1. Possibly you need to `sudo fuser -k 80/tcp` to clean things up after setting up https. 

## Start nginx
1. Start nginx with `sudo service nginx start`. Note that if you get `service: command not found` then whenever this tutorial uses `service` like this you need to use `sudo systemctl start nginx` instead. 
1. In the future, restart nginx with `sudo service nginx restart`. 
1. In case that fails, check the logs at `tail /var/log/long.err.log` or `tail /var/log/long.out.log` to view the error.
1. Try to reach your website. If it doesn't work, try setting `DEBUG = True` in settings and then `sudo supervisorctl restart mysite`, reload page.
1. If it still does not work, restart both nginx (see above) and gunicorn with `sudo supervisorctl restart mysite`

Now go in your browser to your ip address or domain and you should see your website.
If not, check the logs for errors (see [below](#remember)).

### Setting up automatic renewal of https certificates
1. Check the [certbot user guide](https://certbot.eff.org/docs/using.html#automated-renewals) to see if you got automated renewal out of the box. For Ubuntu version >= 17.10, this should be okay. This means that there is a cronjob that runs twice a day to renew all certificates that are about to expire. All we have to do is restart the nginx server after each renewal.
1. Run `sudo vim /etc/cron.d/certbot` and append `--renew-hook "service nginx restart"` so that the last line looks like `0 */12 * * * root test -x /usr/bin/certbot -a \! -d /run/systemd/system && perl -e 'sleep int(rand(43200))' && certbot -q renew --renew-hook "service nginx restart`.
1. Run `sudo certbot renew --dry-run`, this should simulate renewal. If this succeeds without errors, everything should be okay.

To renew certificates manually, do `sudo certbot renew`.

## <a name="remember">To remember</a>
### Django files
After making changes to Django files, run `sudo supervisorctl restart mysite`.
### Django models
After making changes to Django models, in PyCharm start Tools | Run Manage.py Task  and run `makemigrations --settings=mysite.settings.production` and `migrate --settings=mysite.settings.production` (or from the command line, `python3.6 manage.py makemigrations --settings=...`)
### Static files
After making changes to static files run as manage.py task `collectstatic`. If run from the command line, I think you need to activate the virtual environment first.
### Supervisor config
Every time after you change a supervisor config file in `/etc/supervisor/conf.d/mysite.conf`, you have to do `sudo supervisorctl reread` and `sudo supervisorctl update`.
### gunicorn start script
Restart supervisor with `sudo supervisorctl restart mysite`.
### nginx config
After changing nginx config files in `/etc/nginx/sites-available/mysite`, test syntax with `sudo nginx -t` and run `sudo service nginx restart`.
### logs
General logs are viewed with `tail /var/log/long.err.log` or `tail /var/log/long.out.log`, and the nginx log can be found with `tail /opt/mysite_env/mysite/logs/nginx-error.log` as specified in the nginx config file.

If you get an error and nothing appears in the logs, try setting `DEBUG = True` in settings and then `sudo supervisorctl restart mysite`, reload page.
