# Django template project

#### Makes use of
* PostgreSQL
* The [TinyMCE](https://www.tinymce.com/) editor
* HTML templates
* CSS
* Directory structure from [docs.djangoproject.com](https://docs.djangoproject.com/en/1.11/intro/tutorial01/).

## Instructions to run the website locally

* Create a project, and download the files to that location.
* Check that the packages in requirements.txt are installed.
* If you use PyCharm, you can make a Django Server run configuration (instead of running `runserver` all the time). Add an environment variable with name `DJANGO_SETTINGS_MODULE` and value `mysite.settings.development`, assuming the settings are in `development.py` in a folder `settings` in the folder `mysite`. Possibly you need to select your Python interpreter.
* To use a database locally, install PostgreSQL and create a user and then a database; you can use pgAdmin (instructions for pgAdmin 4 2.0) instead of the command prompt to create a user.
 To create a user, right-click on PostgreSQL and choose create Login/Group Role, give it for example the name of your project.
  Create a database by right-clicking on Databases, give it a name for example myproject_db, and under the 'security' tab grant all privileges to the user you just created.
* Replace name, user and password in `DATABASES` in your settings file.
* Use edit - find - replace in path to replace all references to 'mysite' to our own project name. Also rename the 'mysite' module (take care to be consistent with capitalization).
* (Professional edition of PyCharm only) To run `manage.py` tasks, go to settings - Languages and Frameworks - Django and specify your settings file. Then you can use Tools - Run manage.py Task (`CTRL` + `ALT` + `R`) to run tasks like `migrate`.
* Each time after you made changes in your models in models.py, run `makemigrations` and `migrate` to apply the changes to the database. Do that now.
* Also as `manage.py` task, run `createsuperuser --username myname` to create a superuser (for example you) for your website backend.
* Use the run configuration you made or run `runserver`.
* Access the backend by navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
* (tip) If you already have a local website running, changing the port number allows you to keep things separate.

# todo
* Home page extending from base html
* static files settings
* add nginx, supervisor settings etc.

# Deploying on Ubuntu 16.04
We will use nginx and gunicorn.
Make sure that your production settings are kept secret!
It is assumed that the server is already up and running and that you can execute `sudo` commands via SSH or so.