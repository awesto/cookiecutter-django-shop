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
from django.utils.six.moves import input
try:
    import czipfile as zipfile
except ImportError:
    import zipfile


class Command(BaseCommand):
    version = 18
    help = "Download workdir to run a demo of django-SHOP."
    download_url = 'http://downloads.django-shop.org/django-shop-workdir-{version}.zip'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_false',
            dest='interactive',
            default=True,
            help="Do NOT prompt the user for input of any kind.",
        )

    def set_options(self, **options):
        self.interactive = options['interactive']

    def handle(self, verbosity, *args, **options):
        self.set_options(**options)
        fixture1 = '{workdir}/fixtures/products-media.json'.format(workdir=settings.WORK_DIR)
        fixture2 = '{workdir}/fixtures/products-meta.json'.format(workdir=settings.WORK_DIR)
        if os.path.isfile(fixture1) or os.path.isfile(fixture2):
            if self.interactive:
                mesg = """
This will overwrite your workdir for your django-SHOP demo.
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: 
"""
                if input(mesg) != 'yes':
                    raise CommandError("Downloading workdir has been cancelled.")
            else:
                    self.stdout.write(self.style.WARNING("Can not override downloaded data in input-less mode."))
                    return

        extract_to = os.path.join(settings.WORK_DIR, os.pardir)
        msg = "Downloading workdir and extracting to {}. Please wait ..."
        self.stdout.write(msg.format(extract_to))
        download_url = self.download_url.format(version=self.version)
        response = requests.get(download_url, stream=True)
        zip_ref = zipfile.ZipFile(StringIO(response.content))
        try:
            zip_ref.extractall(extract_to)
        finally:
            zip_ref.close()
