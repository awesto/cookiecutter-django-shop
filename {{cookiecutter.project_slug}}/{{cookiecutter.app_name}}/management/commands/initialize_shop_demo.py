# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
from django.conf import settings
from django.core.management.base import BaseCommand
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
        self.clear_compressor_cache()
        initialize_file = os.path.join(settings.WORK_DIR, '.initialize')
        if os.path.isfile(initialize_file):
            self.stdout.write("Initializing project {{ cookiecutter.app_name }}")
            call_command('makemigrations', '{{ cookiecutter.app_name }}')
            call_command('migrate')
            os.remove(initialize_file)
            call_command('loaddata', 'skeleton')
            call_command('shop', 'check-pages', add_recommended=True)
            call_command('assign_iconfonts')
            call_command('download_workdir', interactive=self.interactive)
            call_command('loaddata', 'products-media')
            call_command('import_products')
{%- if cookiecutter.use_sendcloud %}
            call_command('sendcloud_import')
{%- endif %}
        else:
            self.stdout.write("Project {{ cookiecutter.app_name }} already initialized")
            call_command('migrate')
