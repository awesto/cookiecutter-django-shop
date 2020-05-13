from django.conf import settings

from shop.search.documents import ProductDocument

for language, _ in settings.LANGUAGES:
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0,
    }
    ProductDocument(language, settings)