{% if cookiecutter.use_i18n == 'y' -%}
from django.conf import settings as config
{% endif %}
from shop.search.documents import ProductDocument

settings = {
    'number_of_shards': 1,
    'number_of_replicas': 0,
}
{%- if cookiecutter.use_i18n == 'y' %}
for language, _ in settings.LANGUAGES:
    ProductDocument(language=language, settings=settings)
{% else %}
ProductDocument(settings=settings)
{% endif -%}