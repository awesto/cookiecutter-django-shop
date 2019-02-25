# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from cms.utils.copy_plugins import copy_plugins_to
from cms.utils.i18n import get_public_languages
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from django.utils.translation import activate
from cmsplugin_cascade.models import CascadeElement, CascadeClipboard
from shop.management.utils import deserialize_to_placeholder


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, verbosity, filename, *args, **options):
        activate(settings.LANGUAGE_CODE)
        with open(filename, 'r') as fh:
            data = json.load(fh)

        self.stdout.write("Importing products:")
        for number, product in enumerate(data, 1):
            product_model = product.pop('product_model')
            ProductModel = ContentType.objects.get(app_label='myshop', model=product_model)
            class_name = 'myshop.management.serializers.' + ProductModel.model_class().__name__ + 'Serializer'
            serializer_class = import_string(class_name)
            serializer = serializer_class(data=product)
            assert serializer.is_valid(), serializer.errors
            instance = serializer.save()
            self.stdout.write("{}. {}".format(number, instance))
            if product_model == 'commodity':
                languages = get_public_languages()
                try:
                    clipboard = CascadeClipboard.objects.get(identifier=instance.slug)
                except CascadeClipboard.DoesNotExist:
                    pass
                else:
                    deserialize_to_placeholder(instance.placeholder, clipboard.data, languages[0])
                    plugins = list(instance.placeholder.get_plugins(language=languages[0]).order_by('path'))
                    for language in languages[1:]:
                        copy_plugins_to(plugins, instance.placeholder, language)
