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
* If you use PyCharm, you can make a Django Server run configuration (instead of running `runserver` all the time). Add an environment variable with name `DJANGO_SETTINGS_MODULE` and value `mysite.settings`, possibly select Python interpreter.
* To use a database locally, install PostgreSQL and create a user and then a database by following for example [this](https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/optional_postgresql_installation/) tutorial. You can use pgAdmin again instead of the command prompt to create users/databases. You could give the user the name of your project, and under the 'privileges' tab select 'can login' and 'superuser'. Create a database and select the user you just made as owner.
* Use edit - find - replace in path to replace all references to 'mysite' to our own project name. Also rename the 'mysite' module (take care to be consistent with capitalization).
* (Professional edition of PyCharm only) To run `manage.py` tasks, go to settings - Languages & Frameworks - Django and specify your settings file in mysite/settings.py. Then you can use Tools - Run manage.py Task (`Ctrl` + `Alt` + `R`) to run tasks like `migrate`.
* Each time after you made changes in your models in models.py, run `makemigrations` and `migrate` to apply the changes to the database.
* Run `createsuperuser --username myname` to create a superuser for your website backend.
* Use the run configuration you made or run `runserver`.
* Access the backend by navigating to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
* (tip) If you already have a local website running, changing the port number allows you to keep things separate.