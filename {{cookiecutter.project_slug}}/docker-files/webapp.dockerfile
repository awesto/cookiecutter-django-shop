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

# copy project relevant files into container
ADD {{ cookiecutter.app_name }} /web/{{ cookiecutter.app_name }}
COPY requirements.txt /web/requirements.txt
COPY package.json /web/package.json
COPY wsgi.py /web/wsgi.py
COPY manage.py /web/manage.py
COPY worker.py /web/worker.py
{%- if cookiecutter.dockerize == "runserver" %}
COPY docker-files/entrypoint.sh /usr/local/bin/entrypoint.sh
{%- else %}
COPY docker-files/uwsgi.ini /etc/uwsgi.ini
{%- endif %}

# install project specific requirements
RUN pip install -r requirements.txt
{%- if cookiecutter.dockerize != "runserver" %}
RUN npm install
{%- endif %}

{%- if cookiecutter.dockerize == "nginx" %}
# add extra configuration to NGiNX proxy
VOLUME /web/nginx-conf
COPY docker-files/nginx-vhost.conf /web/nginx-conf/{{ cookiecutter.virtual_host }}
{%- endif %}

# handle static and files
ENV DJANGO_STATIC_ROOT=$DJANGO_STATIC_ROOT
ENV DJANGO_WORKDIR=$DJANGO_WORKDIR
RUN mkdir -p $DJANGO_STATIC_ROOT/CACHE
COPY workdir/fixtures/skeleton.json $DJANGO_WORKDIR/fixtures/skeleton.json
COPY workdir/media/filer_public $DJANGO_WORKDIR/media/filer_public
COPY workdir/.initialize $DJANGO_WORKDIR/.initialize
{%- if cookiecutter.dockerize != "runserver" %}
RUN ./manage.py compilescss
RUN ./manage.py collectstatic --noinput --ignore='*.scss'
{%- endif %}

# handle permissions
RUN useradd -M -d /web -s /bin/bash django
RUN chown -R django.django $DJANGO_STATIC_ROOT
RUN chown -R django.django $DJANGO_WORKDIR
RUN chown -R django.django /web/{{ cookiecutter.app_name }}/migrations

{% if cookiecutter.dockerize == "runserver" -%}
USER django
ENTRYPOINT /usr/local/bin/entrypoint.sh
{%- else %}
# keep media files in external volume
VOLUME $DJANGO_WORKDIR
{%- endif %}
