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
    help = _("Initialize the workdir to run the demo of {{ cookiecutter.app_name }}.")

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false',
            dest='interactive',
            default=True,
            help="Do NOT prompt the user for input of any kind.",
        )

    def set_options(self, **options):
        self.interactive = options['interactive']

    def createdb_if_not_exists(self):
        if os.getenv('DATABASE_ENGINE') != 'django.db.backends.postgresql':
            return

        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        except ImportError:
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
        call_command('makemigrations', '{{ cookiecutter.app_name }}')
        call_command('migrate')
        call_command('loaddata', 'skeleton')
        call_command('shop', 'check-pages', add_recommended=True)
        call_command('assign_iconfonts')
        call_command('download_workdir', interactive=self.interactive)
        call_command('loaddata', 'products-media')
        call_command('import_products')
