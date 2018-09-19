FROM python:3.6.6
LABEL Description="Run {{ cookiecutter.project_slug }}" Maintainer="{{ cookiecutter.author_name }}"
RUN mkdir /web
WORKDIR /web
ARG DJANGO_WORKDIR=/web/workdir
ARG DJANGO_STATIC_ROOT=/web/staticfiles

# install packages outside of PyPI
RUN apt-get upgrade -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs optipng jpegoptim
RUN pip install pipenv

# copy project relevant files into container
ADD {{ cookiecutter.app_name }} /web/{{ cookiecutter.app_name }}
COPY wsgi.py /web/wsgi.py
COPY manage.py /web/manage.py
COPY worker.py /web/worker.py
COPY package.json /web/package.json
COPY Pipfile /web/Pipfile
COPY docker-files/uwsgi.ini /web/uwsgi.ini

# install project specific requirements
COPY requirements.txt /web/requirements.txt
RUN pip install -r requirements.txt
RUN pip install https://github.com/jrief/django-cms/archive/fixes/load-fixture.zip
RUN pip install https://github.com/awesto/django-shop/archive/drafts/cms-3.5.zip
RUN npm install

# handle static files
ENV DJANGO_STATIC_ROOT=$DJANGO_STATIC_ROOT
ENV DJANGO_WORKDIR=$DJANGO_WORKDIR
RUN mkdir -p $DJANGO_STATIC_ROOT/CACHE
RUN ./manage.py makemigrations {{ cookiecutter.app_name }}
RUN ./manage.py compilescss
RUN ./manage.py collectstatic --noinput --ignore='*.scss'

# handle permissions
RUN useradd -M -d /web -s /bin/bash django
RUN chown -R django.django $DJANGO_STATIC_ROOT/CACHE

# handle media files in external volume
RUN mkdir -p $DJANGO_WORKDIR
RUN chown -R django.django $DJANGO_WORKDIR

# handle django-SHOP docs
#RUN git clone -b releases/0.13.x https://github.com/awesto/django-shop.git
#RUN cd django-shop/docs && make fragments

# keep media files in external volume
VOLUME $DJANGO_WORKDIR
