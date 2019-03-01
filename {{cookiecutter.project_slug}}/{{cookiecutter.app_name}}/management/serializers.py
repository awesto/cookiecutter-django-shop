# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from shop.serializers.catalog import CMSPagesField, ImagesField, ValueRelatedField
{%- if cookiecutter.products_model == 'polymorphic' %}
from {{ cookiecutter.app_name }}.models import (Commodity, SmartCard, SmartPhoneModel, SmartPhoneVariant,
    Manufacturer, OperatingSystem, ProductPage, ProductImage)
{%- elif cookiecutter.products_model == 'smartcard' %}
from {{ cookiecutter.app_name }}.models import SmartCard, Manufacturer, ProductPage, ProductImage
{%- elif cookiecutter.products_model == 'commodity' %}
from {{ cookiecutter.app_name }}.models import Commodity, ProductPage, ProductImage
{%- endif %}
from .translation import TranslatedFieldsField, TranslatedField, TranslatableModelSerializerMixin


class ProductSerializer(serializers.ModelSerializer):
    product_model = serializers.CharField(read_only=True)
{%- if cookiecutter.products_model != 'commodity' %}
    manufacturer = ValueRelatedField(model=Manufacturer)
{%- endif %}
    caption = TranslatedField()
    cms_pages = CMSPagesField()
    images = ImagesField()

    class Meta:
        exclude = ['id', 'polymorphic_ctype', 'updated_at']

    def create(self, validated_data):
        cms_pages = validated_data.pop('cms_pages')
        images = validated_data.pop('images')
        product = super(ProductSerializer, self).create(validated_data)
        for page in cms_pages:
            ProductPage.objects.create(product=product, page=page)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product


{% if cookiecutter.products_model != 'smartcard' -%}

class CommoditySerializer(TranslatableModelSerializerMixin, ProductSerializer):
    {%- if cookiecutter.products_model == 'commodity' %}
    product_name = TranslatedField()
    slug = TranslatedField()
    {%- endif %}

    class Meta(ProductSerializer.Meta):
        model = Commodity
        exclude = ['id', 'placeholder', 'polymorphic_ctype', 'updated_at']

{%- endif %}{% if cookiecutter.products_model != 'commodity' %}


class SmartCardSerializer(TranslatableModelSerializerMixin, ProductSerializer):
    {%- if cookiecutter.use_i18n == 'y' and cookiecutter.products_model == 'smartcard' %}
    description = TranslatedField()
    {%- else %}
    multilingual = TranslatedFieldsField(
        help_text="Helper to convert multilingual data into single field.",
    )
    {%- endif %}

    class Meta(ProductSerializer.Meta):
        model = SmartCard

{%- endif %}{% if cookiecutter.products_model == 'polymorphic' %}


class SmartphoneVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartPhoneVariant
        fields = ['product_code', 'unit_price', 'storage']


class SmartPhoneModelSerializer(TranslatableModelSerializerMixin, ProductSerializer):
    multilingual = TranslatedFieldsField()
    operating_system = ValueRelatedField(model=OperatingSystem)
    variants = SmartphoneVariantSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        model = SmartPhoneModel

    def create(self, validated_data):
        variants = validated_data.pop('variants')
        product = super(SmartPhoneModelSerializer, self).create(validated_data)
        for variant in variants:
            SmartPhoneVariant.objects.create(product=product, **variant)
        return product
{% endif %}
