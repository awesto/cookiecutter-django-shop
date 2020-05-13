from django.utils.safestring import mark_safe
from rest_framework import serializers
#from shop.search.serializers import ProductSearchSerializer as BaseProductSearchSerializer
{%- if cookiecutter.products_model != 'polymorphic' %}
from shop.serializers.bases import ProductSerializer
{%- else %}
from shop.models.cart import CartModel
from shop.serializers.defaults.catalog import AddToCartSerializer
{%- endif %}
#from {{ cookiecutter.app_name }}.search_indexes import products_index


{% if cookiecutter.products_model == 'commodity' -%}

class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ['product_name', 'slug', 'unit_price', 'product_code']


{% elif cookiecutter.products_model == 'smartcard' -%}

class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ['product_name', 'slug', 'unit_price', 'manufacturer', 'card_type', 'speed',
                  'product_code', 'storage']


{% endif -%}


# class ProductSearchSerializer(BaseProductSearchSerializer):
#     """
#     Serializer to search over all products in this shop
#     """
#     media = serializers.SerializerMethodField()

#     class Meta(BaseProductSearchSerializer.Meta):
#         fields = BaseProductSearchSerializer.Meta.fields + ['media', 'caption']
#         field_aliases = {'q': 'text'}
#         search_fields = ['text']
#         index_classes = myshop_search_index_classes

#     def get_media(self, search_result):
#         return mark_safe(search_result.search_media)


# class CatalogSearchSerializer(BaseProductSearchSerializer):
#     """
#     Serializer to restrict products in the catalog
#     """
#     media = serializers.SerializerMethodField()

#     class Meta(BaseProductSearchSerializer.Meta):
#         fields = BaseProductSearchSerializer.Meta.fields + ['media', 'caption']
#         field_aliases = {'q': 'autocomplete'}
#         search_fields = ['autocomplete']
#         index_classes = myshop_search_index_classes

#     def get_media(self, search_result):
#         return mark_safe(search_result.catalog_media)

{%- if cookiecutter.products_model == 'polymorphic' %}


class AddSmartPhoneToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles SmartPhones
    """

    def get_instance(self, context, data, extra_args):
        product = context['product']
        request = context['request']
        try:
            cart = CartModel.objects.get_from_request(request)
        except CartModel.DoesNotExist:
            cart = None
        try:
            variant = product.get_product_variant(
                product_code=data['product_code'])
        except (TypeError, KeyError, product.DoesNotExist):
            variant = product.variants.first()
        instance = {
            'product': product.id,
            'product_code': variant.product_code,
            'unit_price': variant.unit_price,
            'is_in_cart': bool(product.is_in_cart(cart, product_code=variant.product_code)),
            'extra': {'storage': variant.storage},
            'availability': variant.get_availability(request),
        }
        return instance
{% endif %}
