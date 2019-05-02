FROM python:3.7.3-stretch

# https://docs.docker.com/compose/django/
ENV PYTHONUNBUFFERED 1

RUN mkdir /django_template
WORKDIR /django_template
COPY requirements.txt /django_template/
RUN pip install -r requirements.txt

COPY . /django_template

EXPOSE 8001

# todo Move running commands here?
# Makemigrations and migrate? Which db?
#RUN python manage.py runserver