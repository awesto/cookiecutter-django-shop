# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from django.utils.translation import activate
from myshop.models import Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-o',
            '--output',
            type=str,
            dest='filename',
        )

    def handle(self, verbosity, filename, *args, **options):
        activate(settings.LANGUAGE_CODE)
        data = []
        for product in Product.objects.all():
            ProductModel = ContentType.objects.get(app_label='myshop', model=product.product_model)
            class_name = 'myshop.management.serializers.' + ProductModel.model_class().__name__ + 'Serializer'
            serializer_class = import_string(class_name)
            serializer = serializer_class(product, context={'request': None})
            data.append(serializer.data)
        dump = json.dumps(data, indent=2)
        if filename:
            with open(filename, 'w') as fh:
                fh.write(dump)
        else:
            self.stdout.write(dump)
