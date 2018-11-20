# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.safestring import mark_safe
from rest_framework import serializers
from shop.search.serializers import ProductSearchSerializer as BaseProductSearchSerializer
from shop.serializers.bases import ProductSerializer
from shop.serializers.defaults import AddToCartSerializer

{% if cookiecutter.products_model in ['smartcard', 'polymorphic'] %}
from {{ cookiecutter.app_name }} import SmartCard, SmartPhoneModel
{% endif %}

from {{ cookiecutter.app_name }}.search_indexes import myshop_search_index_classes


class ProductSummarySerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ['id', 'product_name', 'product_url', 'product_model', 'price', 'media', 'caption']

{% if cookiecutter.products_model == 'commodity' %}

class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ['product_name', 'slug', 'unit_price', 'product_code']

{% elif cookiecutter.products_model == 'smartcard' %}

class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ['product_name', 'slug', 'unit_price', 'manufacturer', 'card_type', 'speed',
                  'product_code', 'storage']

{% endif %}

class ProductSearchSerializer(BaseProductSearchSerializer):
    """
    Serializer to search over all products in this shop
    """
    media = serializers.SerializerMethodField()

    class Meta(BaseProductSearchSerializer.Meta):
        fields = BaseProductSearchSerializer.Meta.fields + ['media', 'caption']
        field_aliases = {'q': 'text'}
        search_fields = ['text']
        index_classes = myshop_search_index_classes

    def get_media(self, search_result):
        return mark_safe(search_result.search_media)


class CatalogSearchSerializer(BaseProductSearchSerializer):
    """
    Serializer to restrict products in the catalog
    """
    media = serializers.SerializerMethodField()

    class Meta(BaseProductSearchSerializer.Meta):
        fields = BaseProductSearchSerializer.Meta.fields + ['media', 'caption']
        field_aliases = {'q': 'autocomplete'}
        search_fields = ['autocomplete']
        index_classes = myshop_search_index_classes

    def get_media(self, search_result):
        return mark_safe(search_result.catalog_media)

{% if cookiecutter.products_model in ['smartcard', 'polymorphic'] %}
class SmartCardSerializer(ProductSerializer):
    class Meta:
        model = SmartCard
        fields = ['product_name', 'slug', 'unit_price', 'manufacturer', 'card_type', 'speed',
                  'product_code', 'storage']

class SmartPhoneSerializer(ProductSerializer):
    class Meta:
        model = SmartPhoneModel
        fields = ['product_name', 'slug', 'battery_type', 'battery_capacity']

class AddSmartPhoneToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles SmartPhones
    """
    def get_instance(self, context, data, extra_args):
        product = context['product']
        if data is empty:
            product_code = None
            extra = {}
        else:
            product_code = data.get('product_code')
            extra = data.get('extra', {})
        try:
            variant = product.get_product_variant(product_code=product_code)
        except product.DoesNotExist:
            variant = product.variants.first()
        extra.update(storage=variant.storage)
        instance = {
            'product': product.id,
            'product_code': variant.product_code,
            'unit_price': variant.unit_price,
            'extra': extra,
        }
        return instance

{% endif %}
