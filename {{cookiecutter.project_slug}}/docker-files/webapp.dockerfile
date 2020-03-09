FROM python:3.6.6
LABEL Description="{{ cookiecutter.description }}" Maintainer="{{ cookiecutter.author_name }}"
RUN mkdir /web
WORKDIR /web
ARG DJANGO_WORKDIR=/web/workdir
ARG DJANGO_STATIC_ROOT=/web/staticfiles

# install packages outside of PyPI
RUN apt-get upgrade -y
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs optipng jpegoptim
RUN pip install --upgrade pip
{%- if cookiecutter.pip_dependency_manager == "poetry" %}
# official install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
{%- endif %}
{%- if cookiecutter.dockerize == "runserver" %}
COPY docker-files/entrypoint.sh /usr/local/bin/entrypoint.sh
{%- else %}
# copy project relevant files into container
ADD {{ cookiecutter.app_name }} /web/{{ cookiecutter.app_name }}
COPY package.json /web/package.json
COPY wsgi.py /web/wsgi.py
COPY manage.py /web/manage.py
COPY worker.py /web/worker.py
COPY docker-files/uwsgi.ini /etc/uwsgi.ini
{%- endif %}

{%- if cookiecutter.pip_dependency_manager == "pipenv" %}
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
{%- elif cookiecutter.pip_dependency_manager == "poetry" %}
COPY pyproject.toml /web/pyproject.toml
RUN $HOME/.poetry/bin/poetry config settings.virtualenvs.create false 
RUN $HOME/.poetry/bin/poetry install 
{%- endif %}

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
{%- if cookiecutter.dockerize != "runserver" %}
COPY workdir/fixtures/skeleton.json $DJANGO_WORKDIR/fixtures/skeleton.json
COPY workdir/media/filer_public $DJANGO_WORKDIR/media/filer_public
COPY workdir/.initialize $DJANGO_WORKDIR/.initialize
{%- endif %}
{%- if cookiecutter.debug == "n" %}
RUN ./manage.py compilescss
RUN ./manage.py collectstatic --noinput --ignore='*.scss'
{%- endif %}

# run Django as different user
RUN useradd -M -d /web -s /bin/bash django

{% if cookiecutter.dockerize == "runserver" -%}
USER django
{%- else %}
# handle permissions
RUN chown -R django.django $DJANGO_STATIC_ROOT
RUN chown -R django.django $DJANGO_WORKDIR
RUN chown -R django.django /web/{{ cookiecutter.app_name }}/migrations

# keep media files in external volume
VOLUME $DJANGO_WORKDIR
{%- endif %}
