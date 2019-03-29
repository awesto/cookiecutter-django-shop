#!/bin/bash
set -e

{%- if cookiecutter.dockerize == "runserver" %}
npm install
/web/manage.py initialize_shop_demo --noinput
echo "$@"
exec /web/manage.py runserver 0.0.0.0:9009
{%- else %}
exec "$@"
{%- endif %}
