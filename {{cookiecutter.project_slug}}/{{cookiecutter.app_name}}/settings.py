# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Django settings for {{ cookiecutter.app_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from decimal import Decimal
import os
import six
from django.urls import reverse_lazy
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from cmsplugin_cascade.bootstrap4.mixins import BootstrapUtilities

SHOP_APP_LABEL = '{{ cookiecutter.app_name }}'
BASE_DIR = os.path.dirname(__file__)

# Root directory for this django project
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir))

# Directory where working files, such as media and databases are kept
WORK_DIR = os.environ.get('DJANGO_WORKDIR', os.path.abspath(os.path.join(PROJECT_ROOT, os.path.pardir, 'workdir')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

ADMINS = (("The Merchant", 'the.merchant@example.com'),)

# SECURITY WARNING: in production, inject the secret key through the environment
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '!!!SET DJANGO_SECRET_KEY!!!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG'))

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = '{{ cookiecutter.timezone }}'

USE_THOUSAND_SEPARATOR = True

# Application definition

# replace django.contrib.auth.models.User by implementation
# allowing to login via email address
AUTH_USER_MODEL = 'email_auth.User'

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
        'min_length': 6,
    }
}]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'email_auth',
    'polymorphic',
    # deprecated: 'djangocms_admin_style',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'djangocms_text_ckeditor',
    'django_select2',
    'cmsplugin_cascade',
    'cmsplugin_cascade.clipboard',
    'cmsplugin_cascade.sharable',
    'cmsplugin_cascade.extra_fields',
    'cmsplugin_cascade.icon',
    'cmsplugin_cascade.segmentation',
    'cms_bootstrap',
    'adminsortable2',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_fsm',
    'fsm_admin',
    'djng',
    'cms',
    'menus',
    'treebeard',
    'compressor',
    'sekizai',
    'sass_processor',
    'django_filters',
    'filer',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    {% if cookiecutter.use_i18n == 'y' %}'parler',{% endif %}
    'post_office',
    'haystack',
    'shop_stripe',
    'shop_sendcloud',
    'shop',
#    'html_email',
    '{{ cookiecutter.app_name }}',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shop.middleware.CustomerMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

{%- if cookiecutter.use_i18n == 'y' %}
    {%- set shop_tutorial = 'i18n_' + cookiecutter.products_model %}
{%- else %}
    {%- set shop_tutorial = cookiecutter.products_model %}
{%- endif %}

# MIGRATION_MODULES = {
#     '{{ cookiecutter.app_name }}': '{{ cookiecutter.app_name }}.migrations.{}'.format('{{ shop_tutorial }}')
# }

ROOT_URLCONF = '{{ cookiecutter.app_name }}.urls'

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(WORK_DIR, '{{ shop_tutorial }}', 'db.sqlite3'),
    }
}
{%- if cookiecutter.use_docker == 'y' %}
if os.getenv('DATABASE_ENGINE') == 'django.db.backends.postgresql':
    DATABASES['default'].update({
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'djangoshop'),
        'USER': os.getenv('DATABASE_USER', 'djangoshop'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', 5432),
    })
{%- endif %}


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'en'
{% if cookiecutter.use_i18n == 'y' %}
USE_I18N = True

LANGUAGES = [
    ('en', "English"),
    ('de', "Deutsch"),
]

PARLER_DEFAULT_LANGUAGE = 'en'

PARLER_LANGUAGES = {
    1: (
        {'code': 'de'},
        {'code': 'en'},
    ),
    'default': {
        'fallbacks': ['de', 'en'],
    },
}

CMS_LANGUAGES = {
    'default': {
        'fallbacks': ['en', 'de'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
    1: ({
        'public': True,
        'code': 'en',
        'hide_untranslated': False,
        'name': 'English',
        'redirect_on_fallback': True,
    }, {
        'public': True,
        'code': 'de',
        'hide_untranslated': False,
        'name': 'Deutsch',
        'redirect_on_fallback': True,
    },)
}
{% else %}
USE_I18N = False
{% endif %}

USE_L10N = True

USE_TZ = True

USE_X_FORWARDED_HOST = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(WORK_DIR, '{{ shop_tutorial }}', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', os.path.join(WORK_DIR, 'static'))

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    '{{ cookiecutter.app_name }}.finders.FileSystemFinder',  # or 'django.contrib.staticfiles.finders.FileSystemFinder',
    '{{ cookiecutter.app_name }}.finders.AppDirectoriesFinder',  # or 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    ('node_modules', os.path.join(PROJECT_ROOT, 'node_modules')),
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [],
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.template.context_processors.csrf',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'sekizai.context_processors.sekizai',
            'cms.context_processors.cms_settings',
            'shop.context_processors.customer',
            'shop.context_processors.shop_settings',
            'shop_stripe.context_processors.public_keys',
        )
    }
#}, {
#    'BACKEND': 'html_email.template.backends.html_email.EmailTemplates',
#    'APP_DIRS': True,
#    'DIRS': [],
#    'OPTIONS': {
#        'context_processors': [
#            'django.contrib.auth.context_processors.auth',
#            'django.template.context_processors.debug',
#            'django.template.context_processors.i18n',
#            'django.template.context_processors.media',
#            'django.template.context_processors.static',
#            'django.template.context_processors.tz',
#            'django.template.context_processors.request',
#        ]
#    }
}]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REDIS_HOST = os.getenv('REDIS_HOST')

if REDIS_HOST:
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_SAVE_EVERY_REQUEST = True

    SESSION_REDIS = {
        'host': REDIS_HOST,
        'port': 6379,
        'db': 0,
        'prefix': 'session-{{ shop_tutorial }}',
        'socket_timeout': 1
    }

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': 'redis://{}:6379/1'.format(REDIS_HOST),
             'OPTIONS': {
                 'PICKLE_VERSION': 2 if six.PY2 else -1,
             }
        },
        'compressor': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': 'redis://{}:6379/2'.format(REDIS_HOST),
        },
        'select2': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }

    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 3600

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'formatters': {
        'simple': {
            'format': '[%(asctime)s %(module)s] %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'post_office': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

SILENCED_SYSTEM_CHECKS = ['auth.W004']

FIXTURE_DIRS = [os.path.join(WORK_DIR, '{{ shop_tutorial }}', 'fixtures')]

############################################
# settings for sending mail

EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'localhost')
EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT', 25)
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_USER', 'no-reply@localhost')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_PASSWORD', 'smtp-secret')
EMAIL_USE_TLS = bool(os.getenv('DJANGO_EMAIL_USE_TLS', '1'))
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_EMAIL_FROM', 'no-reply@localhost')
EMAIL_REPLY_TO = os.getenv('DJANGO_EMAIL_REPLY_TO', 'info@localhost')
EMAIL_BACKEND = 'post_office.EmailBackend'


############################################
# settings for third party Django apps

NODE_MODULES_URL = STATIC_URL + 'node_modules/'

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(PROJECT_ROOT, 'node_modules'),
]

COERCE_DECIMAL_TO_STRING = True

FSM_ADMIN_FORCE_PERMIT = True

ROBOTS_META_TAGS = ('noindex', 'nofollow')

SERIALIZATION_MODULES = {'json': str('shop.money.serializers')}

############################################
# settings for django-restframework and plugins

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'shop.rest.money.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # can be disabled for production environments
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
#    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#    'PAGE_SIZE': 16,
}

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'shop.serializers.auth.LoginSerializer',
}

############################################
# settings for storing session data

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_SAVE_EVERY_REQUEST = True


############################################
# settings for storing files and images

FILER_ADMIN_ICON_SIZES = ('16', '32', '48', '80', '128')

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

FILER_DUMP_PAYLOAD = False

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

THUMBNAIL_HIGH_RESOLUTION = False

THUMBNAIL_OPTIMIZE_COMMAND = {
    'gif': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}',
    'png': '/usr/bin/optipng {filename}'
}

THUMBNAIL_PRESERVE_EXTENSIONS = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)


############################################
# settings for django-cms and its plugins

CMS_TEMPLATES = [
    ('{{ cookiecutter.app_name }}/pages/default.html', _("Default Page")),
    ('{{ cookiecutter.app_name }}/pages/test.html', _("Test Page")),  # to show strides rendering via {% raw %}{% render_cascade ... %}{% endraw %}
]

CMS_CACHE_DURATIONS = {
    'content': 600,
    'menus': 3600,
    'permissions': 86400,
}

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {
    'Breadcrumb': {
        'plugins': ['BreadcrumbPlugin'],
        'parent_classes': {'BreadcrumbPlugin': None},
    },
    'Commodity Details': {
        'plugins': ['BootstrapContainerPlugin', 'BootstrapJumbotronPlugin'],
        'parent_classes': {
            'BootstrapContainerPlugin': None,
            'BootstrapJumbotronPlugin': None,
        },
    },
    'Main Content': {
        'plugins': ['BootstrapContainerPlugin', 'BootstrapJumbotronPlugin'],
        'parent_classes': {
            'BootstrapContainerPlugin': None,
            'BootstrapJumbotronPlugin': None,
            'TextLinkPlugin': ['TextPlugin', 'AcceptConditionPlugin'],
        },
    },
    'Static Footer': {
        'plugins': ['BootstrapContainerPlugin', ],
        'parent_classes': {
            'BootstrapContainerPlugin': None,
        },
    },
}

CMSPLUGIN_CASCADE_PLUGINS = [
    'cmsplugin_cascade.bootstrap4',
    'cmsplugin_cascade.segmentation',
    'cmsplugin_cascade.generic',
    'cmsplugin_cascade.icon',
    'cmsplugin_cascade.leaflet',
    'cmsplugin_cascade.link',
    'shop.cascade',
]

CMSPLUGIN_CASCADE = {
    'link_plugin_classes': [
        'shop.cascade.plugin_base.CatalogLinkPluginBase',
        'cmsplugin_cascade.link.plugin_base.LinkElementMixin',
        'shop.cascade.plugin_base.CatalogLinkForm',
    ],
    'alien_plugins': ['TextPlugin', 'TextLinkPlugin', 'AcceptConditionPlugin'],
    'bootstrap4': {
        'template_basedir': 'angular-ui',
    },
    'plugins_with_extra_render_templates': {
        'CustomSnippetPlugin': [
            ('shop/catalog/product-heading.html', _("Product Heading")),
            ('{{ cookiecutter.app_name }}/catalog/manufacturer-filter.html', _("Manufacturer Filter")),
        ],
        'ShopAddToCartPlugin': [
            (None, _("Default")),
            ('{{ cookiecutter.app_name }}/catalog/commodity-add2cart.html', _("Add Commodity to Cart")),
        ],
    },
    'plugins_with_sharables': {
        'BootstrapImagePlugin': ['image_shapes', 'image_width_responsive', 'image_width_fixed',
                                 'image_height', 'resize_options'],
        'BootstrapPicturePlugin': ['image_shapes', 'responsive_heights', 'image_size', 'resize_options'],
    },
#    'plugins_with_extra_mixins': {
#        'BootstrapRowPlugin': BootstrapUtilities(BootstrapUtilities.margins),
#    },
#     "The translation infrastructure cannot be initialized before the "
#    django.core.exceptions.AppRegistryNotReady: The translation infrastructure cannot be initialized before the apps registry is ready.
#    Check that you don't make non-lazy gettext calls at import time.
#    in variable  choices_format       python3.6/site-packages/cmsplugin_cascade/bootstrap4/mixins.py", line 101, in margins
    'leaflet': {
        'tilesURL': 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
        'accessToken': 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
        'apiKey': 'AIzaSyD71sHrtkZMnLqTbgRmY_NsO0A9l9BQmv4',
    },
    'bookmark_prefix': '/',
    'segmentation_mixins': [
        ('shop.cascade.segmentation.EmulateCustomerModelMixin', 'shop.cascade.segmentation.EmulateCustomerAdminMixin'),
    ],
    'allow_plugin_hiding': True,
}

CKEDITOR_SETTINGS = {
    'language': '{% raw %}{{ language }}{% endraw %}',
    'skin': 'moono-lisa',
    'toolbar': 'CMS',
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
    'stylesSet': format_lazy('default:{}', reverse_lazy('admin:cascade_texticon_wysiwig_config')),
}

CKEDITOR_SETTINGS_CAPTION = {
    'language': '{% raw %}{{ language }}{% endraw %}',
    'skin': 'moono-lisa',
    'height': 70,
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['Format', 'Styles'],
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['Source']
    ],
}

CKEDITOR_SETTINGS_DESCRIPTION = {
    'language': '{% raw %}{{ language }}{% endraw %}',
    'skin': 'moono-lisa',
    'height': 250,
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
}

SELECT2_CSS = 'node_modules/select2/dist/css/select2.min.css'
SELECT2_JS = 'node_modules/select2/dist/js/select2.min.js'


COMPRESS_CACHE_BACKEND = 'compressor'

#############################################
# settings for full index text search (Haystack)

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://{}:9200/'.format(ELASTICSEARCH_HOST),
        'INDEX_NAME': '{{ cookiecutter.app_name }}-{{ shop_tutorial }}-en',
    },
{%- if cookiecutter.use_i18n == 'y' %}
    'de': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://{}:9200/'.format(ELASTICSEARCH_HOST),
        'INDEX_NAME': '{{ cookiecutter.app_name }}-{{ shop_tutorial }}-de',
    }
{% endif -%}
}

HAYSTACK_ROUTERS = [
    'shop.search.routers.LanguageRouter',
]

############################################
# settings for django-shop and its plugins

SHOP_VALUE_ADDED_TAX = Decimal(19)
SHOP_DEFAULT_CURRENCY = 'EUR'
SHOP_PRODUCT_SUMMARY_SERIALIZER = '{{ cookiecutter.app_name }}.serializers.ProductSummarySerializer'
SHOP_CART_MODIFIERS = [
{%- if cookiecutter.products_model == 'polymorphic' %}
    '{{ cookiecutter.app_name }}.polymorphic_modifiers.MyShopCartModifier',
{%- else %}
    'shop.modifiers.defaults.DefaultCartModifier',
{%- endif %}
    '{{ cookiecutter.app_name }}.modifiers.PostalShippingModifier',
]

SHOP_EDITCART_NG_MODEL_OPTIONS = "{updateOn: 'default blur', debounce: {'default': 2500, 'blur': 0}}"

SHOP_ORDER_WORKFLOWS = [
    'shop.payment.workflows.ManualPaymentWorkflowMixin',
    'shop.payment.workflows.CancelOrderWorkflowMixin',
{%- if cookiecutter.products_model == 'polymorphic' %}
    'shop.shipping.worflows.PartialDeliveryWorkflowMixin',
{%- else %}
#    'shop.shipping.workflows.CommissionGoodsWorkflowMixin',
{%- endif %}
]

if 'shop_stripe' in INSTALLED_APPS:
    SHOP_CART_MODIFIERS.append('{{ cookiecutter.app_name }}.modifiers.StripePaymentModifier')
    SHOP_ORDER_WORKFLOWS.append('shop_stripe.payment.OrderWorkflowMixin')

if 'shop_sendcloud' in INSTALLED_APPS:
    SHOP_CART_MODIFIERS.append('shop_sendcloud.modifiers.SendcloudShippingModifiers')
    SHOP_ORDER_WORKFLOWS.extend(['shop_sendcloud.workflows.SingularOrderWorkflowMixin',
                                 'shop.shipping.workflows.CommissionGoodsWorkflowMixin'])


SHOP_CART_MODIFIERS.extend([
    'shop.modifiers.taxes.CartExcludedTaxModifier',
    '{{ cookiecutter.app_name }}.modifiers.CustomerPickupModifier',
    'shop.payment.modifiers.PayInAdvanceModifier',
    'shop.modifiers.defaults.WeightedCartModifier',
])

SHOP_STRIPE = {
    'PUBKEY': 'pk_test_HlEp5oZyPonE21svenqowhXp',
    'APIKEY': 'sk_test_xUdHLeFasmOUDvmke4DHGRDP',
    'PURCHASE_DESCRIPTION': _("Thanks for purchasing at {{ cookiecutter.app_name }}"),
}

SHOP_STRIPE_PREFILL = True

SHOP_SENDCLOUD = {
    'API_KEY': os.getenv('SENDCLOUD_PUBLIC_KEY'),
    'API_SECRET': os.getenv('SENDCLOUD_SECRET_KEY'),
}

SHOP_CASCADE_FORMS = {
    'CustomerForm': '{{ cookiecutter.app_name }}.forms.CustomerForm',
}

SHOP_MANUAL_SHIPPING_ID = False
