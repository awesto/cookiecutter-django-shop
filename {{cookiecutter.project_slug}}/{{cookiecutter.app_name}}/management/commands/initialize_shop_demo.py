# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
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

{%- if cookiecutter.use_compressor == 'y' %}

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
{%- endif %}

    def handle(self, verbosity, *args, **options):
        self.set_options(**options)
{%- if cookiecutter.use_compressor == 'y' %}
        self.clear_compressor_cache()
{%- endif %}
        call_command('migrate')
        initialize_file = os.path.join(settings.WORK_DIR, '.initialize')
        if os.path.isfile(initialize_file):
            self.stdout.write("Initializing project {{ cookiecutter.app_name }}")
            call_command('makemigrations', '{{ cookiecutter.app_name }}')
            call_command('migrate')
            os.remove(initialize_file)
            call_command('loaddata', 'skeleton')
            call_command('shop', 'check-pages', add_recommended=True)
            call_command('assign_iconfonts')
            call_command('create_social_icons')
            print(cookiecutter.__dict__)
            {%- if not cookiecutter.noinput %}
            call_command('download_workdir', interactive=self.interactive)
            call_command('loaddata', 'products-media')
            {%- endif %}
            call_command('import_products')
{%- if cookiecutter.products_model == 'polymorphic' %}
            self.create_polymorphic_subcategories()
{%- endif %}
{%- if cookiecutter.stock_management == 'inventory' %}
            call_command('initialize_inventories')
{%- endif %}
{%- if cookiecutter.use_sendcloud == 'y' %}
            try:
                call_command('sendcloud_import')
            except CommandError:
                pass
{%- endif %}
        else:
            self.stdout.write("Project {{ cookiecutter.app_name }} already initialized")
            call_command('migrate')

{%- if cookiecutter.products_model == 'polymorphic' %}

    def create_polymorphic_subcategories(self):
        from cms.models.pagemodel import Page
        from shop.management.commands.shop import Command as ShopCommand
        from {{ cookiecutter.app_name }}.models import Commodity, SmartCard, SmartPhoneModel

        apphook = ShopCommand.get_installed_apphook('CatalogListCMSApp')
        catalog_pages = Page.objects.drafts().filter(application_urls=apphook.__class__.__name__)
        assert catalog_pages.count() == 1, "There should be only one catalog page"
        self.create_subcategory(apphook, catalog_pages.first(), "Earphones", Commodity)
        self.create_subcategory(apphook, catalog_pages.first(), "Smart Cards", SmartCard)
        self.create_subcategory(apphook, catalog_pages.first(), "Smart Phones", SmartPhoneModel)

    def create_subcategory(self, apphook, parent_page, title, product_type):
        from cms.api import create_page
        from cms.constants import TEMPLATE_INHERITANCE_MAGIC
        from cms.utils.i18n import get_public_languages
        from shop.management.commands.shop import Command as ShopCommand
        from shop.models.product import ProductModel
        from shop.models.related import ProductPageModel

        language = get_public_languages()[0]
        page = create_page(
            title,
            TEMPLATE_INHERITANCE_MAGIC,
            language,
            apphook=apphook,
            created_by="manage.py initialize_shop_demo",
            in_navigation=True,
            parent=parent_page,
        )
        ShopCommand.publish_in_all_languages(page)
        page = page.get_public_object()
        for product in ProductModel.objects.instance_of(product_type):
            ProductPageModel.objects.create(page=page, product=product)

{%- endif %}
