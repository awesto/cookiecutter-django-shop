from django.contrib.sitemaps import Sitemap
from django.conf import settings
{%- if cookiecutter.products_model == 'commodity' %}
from shop.models.defaults.commodity import Commodity as Product
{%- elif cookiecutter.products_model == 'smartcard' %}
from {{ cookiecutter.app_name }}.models import SmartCard as Product
{%- elif cookiecutter.products_model == 'polymorphic' %}
from {{ cookiecutter.app_name }}.models import Product
{% endif %}

class ProductSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    i18n = settings.USE_I18N

    def items(self):
        return Product.objects.filter(active=True)
