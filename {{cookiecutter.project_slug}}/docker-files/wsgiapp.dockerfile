FROM python:3.6.6
LABEL Description="{{ cookiecutter.description }}" Maintainer="{{ cookiecutter.author_name }}"
RUN mkdir /web
WORKDIR /web
ARG DJANGO_WORKDIR=/web/workdir
ARG DJANGO_STATIC_ROOT=/web/staticfiles

# install packages outside of PyPI
RUN apt-get upgrade -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs optipng jpegoptim
RUN pip install --upgrade pip

# install project specific requirements
COPY requirements.txt /web/requirements.txt
RUN pip install -r requirements.txt
COPY package.json /web/package.json
RUN npm install

# copy project relevant files into container
ADD {{ cookiecutter.app_name }} /web/{{ cookiecutter.app_name }}
COPY wsgi.py /web/wsgi.py
COPY manage.py /web/manage.py
COPY worker.py /web/worker.py
COPY docker-files/uwsgi.ini /web/uwsgi.ini

# add extra configuration to NGiNX proxy
VOLUME /web/nginx-conf
COPY docker-files/nginx-vhost.conf /web/nginx-conf/{{ cookiecutter.virtual_host }}

# handle static and files
ENV DJANGO_STATIC_ROOT=$DJANGO_STATIC_ROOT
ENV DJANGO_WORKDIR=$DJANGO_WORKDIR
RUN mkdir -p $DJANGO_STATIC_ROOT/CACHE
COPY workdir/fixtures/skeleton.json $DJANGO_WORKDIR/fixtures/skeleton.json
COPY workdir/media/filer_public $DJANGO_WORKDIR/media/filer_public
COPY workdir/.initialize $DJANGO_WORKDIR/.initialize
RUN ./manage.py compilescss
RUN ./manage.py collectstatic --noinput --ignore='*.scss'

# handle permissions
RUN useradd -M -d /web -s /bin/bash django
RUN chown -R django.django $DJANGO_STATIC_ROOT
RUN chown -R django.django $DJANGO_WORKDIR
RUN chown -R django.django /web/{{ cookiecutter.app_name }}/migrations

# keep media files in external volume
VOLUME $DJANGO_WORKDIR
