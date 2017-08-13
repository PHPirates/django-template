# Django template project

#### Makes use of
* PostgreSQL
* HTML templates
* CSS
* Directory structure from [docs.djangoproject.com](https://docs.djangoproject.com/en/1.11/intro/tutorial01/).

## Instructions to run the website locally

* If you use PyCharm, you can make a run configuration (instead of running `runserver` all the time) by adding an environment variable with name `DJANGO_SETTINGS_MODULE` and value `mysite.settings`. 
* To use a database locally, install PostgreSQL and create a database by following for example [this](https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/optional_postgresql_installation/) tutorial. You can use pgAdmin again instead of the command prompt to create users/databases.
* (Professional edition of PyCharm only) To run `manage.py` tasks, go to settings - Languages & Frameworks - Django and specify your settings file in mysite/settings.py. Then you can use Tools - Run manage.py Task (`Ctrl` + `Alt` + `R`) to run tasks like `migrate`.
* There, run `migrate` to apply migrations.
* Run `createsuperuser --username myname` to create a superuser for your website backend.
* Use the run configuration you made or run `runserver`.
* Access the backend by navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)