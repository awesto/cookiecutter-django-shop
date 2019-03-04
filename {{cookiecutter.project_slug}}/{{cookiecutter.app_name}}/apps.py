# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class {{ cookiecutter.appName }}(AppConfig):
    name = '{{ cookiecutter.app_name }}'
    verbose_name = _("My Shop")
    logger = logging.getLogger('{{ cookiecutter.app_name }}')

    def ready(self):
        if not os.path.isdir(settings.STATIC_ROOT):
            os.makedirs(settings.STATIC_ROOT)
        if not os.path.isdir(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        if hasattr(settings, 'COMPRESS_ROOT') and not os.path.isdir(settings.COMPRESS_ROOT):
           os.makedirs(settings.COMPRESS_ROOT)
        as_i18n = {% if cookiecutter.use_i18n == 'y' %}" as I18N"{% else %}""{% endif %}
        self.logger.info("Running as {{ cookiecutter.products_model }}{}".format(as_i18n))
