# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import requests
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.utils.six.moves import input
try:
    import czipfile as zipfile
except ImportError:
    import zipfile


class Command(BaseCommand):
    version = 14
    help = _("Initialize the workdir to run the demo of {{ cookiecutter.app_name }}.")
    download_url = 'http://downloads.django-shop.org/django-shop-workdir_{tutorial}-{version}.zip'
    pwd = b'z7xv'
    tutorial = "{% if cookiecutter.use_i18n == 'y' %}i18n_{% endif %}{{ cookiecutter.products_model }}"

    def __init__(self, **kwargs):
        if '{{ cookiecutter.app_name }}' != 'myshop':
            msg = "Can only initialize django-SHOP if cookiecutter template was created with app_name='myshop'."
            raise CommandError(msg)
        super(Command, self).__init__(**kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--noinput', '--no-input', action='store_false', dest='interactive',
                            default=True, help="Do NOT prompt the user for input of any kind.")

    def set_options(self, **options):
        self.interactive = options['interactive']

    def createdb_if_not_exists(self):
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        except ImportError:
            return
        if os.getenv('DATABASE_ENGINE') != 'django.db.backends.postgresql':
            return

        dbname = os.getenv('DATABASE_NAME')
        if dbname is None:
            return
        host = os.getenv('DATABASE_HOST')
        user = os.getenv('DATABASE_USER')
        password = os.getenv('DATABASE_PASSWORD')
        try:
            con = psycopg2.connect(dbname=dbname, host=host, user=user, password=password)
        except psycopg2.OperationalError:
            con = psycopg2.connect(host=host, user=user, password=password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute('CREATE DATABASE {};'.format(dbname))
        finally:
            con.close()

    def clear_compressor_cache(self):
        from django.core.cache import caches
        from django.core.cache.backends.base import InvalidCacheBackendError
        from compressor.conf import settings

        cache_dir = os.path.join(settings.STATIC_ROOT, settings.COMPRESS_OUTPUT_DIR)
        if settings.COMPRESS_ENABLED is False or not os.path.isdir(cache_dir) or os.listdir(cache_dir) != []:
            return
        try:
            caches['compressor'].clear()
        except InvalidCacheBackendError:
            pass

    def handle(self, verbosity, *args, **options):
        self.set_options(**options)
        self.createdb_if_not_exists()
        self.clear_compressor_cache()
        call_command('migrate')

        fixture = '{workdir}/{tutorial}/fixtures/myshop.json'.format(workdir=settings.WORK_DIR, tutorial=self.tutorial)

        if self.interactive:
            mesg = ("\nThis will overwrite your workdir and install a new database for the django-SHOP demo: {tutorial}\n"
                    "Are you sure you want to do this?\n\n"
                    "Type 'yes' to continue, or 'no' to cancel: ").format(tutorial=self.tutorial)
            if input(mesg) != 'yes':
                raise CommandError("SHOP initialization cancelled.")
        else:
            if os.path.isfile(fixture):
                self.stdout.write(self.style.WARNING("Can not override downloaded data in input-less mode."))
                return

        extract_to = os.path.join(settings.WORK_DIR, os.pardir)
        msg = "Downloading workdir and extracting to {}. Please wait ..."
        self.stdout.write(msg.format(extract_to))
        download_url = self.download_url.format(tutorial=self.tutorial, version=self.version)
        response = requests.get(download_url, stream=True)
        zip_ref = zipfile.ZipFile(StringIO(response.content))
        try:
            zip_ref.extractall(extract_to, pwd=self.pwd)
        finally:
            zip_ref.close()

        call_command('loaddata', fixture)
