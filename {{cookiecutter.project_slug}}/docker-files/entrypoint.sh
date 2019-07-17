#!/bin/bash
set -e
exec /web/poetry shell
echo "HHHHHHH"
npm install
/web/manage.py initialize_shop_demo --noinput
exec /web/manage.py runserver 0.0.0.0:9009
