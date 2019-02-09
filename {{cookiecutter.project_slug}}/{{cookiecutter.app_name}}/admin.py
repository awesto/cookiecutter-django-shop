# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Max
from django.template.context import Context
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template

{%- if cookiecutter.use_i18n == 'y' %}
from parler.admin import TranslatableAdmin
{%- endif %}
from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin

from shop.admin.defaults import customer
from shop.admin.defaults.order import OrderAdmin
from shop.models.defaults.order import Order
from shop.admin.order import PrintOrderAdminMixin
from shop.admin.delivery import DeliveryOrderAdminMixin


{%- if cookiecutter.products_model == 'commodity' %}
from shop.admin.defaults import commodity
{%- elif cookiecutter.products_model in ['smartcard', 'polymorphic'] %}
from adminsortable2.admin import SortableAdminMixin, PolymorphicSortableAdminMixin
from shop.admin.product import CMSPageAsCategoryMixin, ProductImageInline, InvalidateProductCacheMixin, CMSPageFilter
from shop_sendcloud.admin import SendCloudOrderAdminMixin
    {%- if cookiecutter.products_model == 'polymorphic' %}
from polymorphic.admin import (PolymorphicParentModelAdmin, PolymorphicChildModelAdmin,
                               PolymorphicChildModelFilter)
from {{ cookiecutter.app_name }}.models import Product, Commodity, SmartPhoneVariant, SmartPhoneModel, OperatingSystem
    {%- endif %}
from {{ cookiecutter.app_name }}.models import Manufacturer, SmartCard
{% endif %}

admin.site.site_header = "{{ cookiecutter.project_name }} Administration"

@admin.register(Order)
class OrderAdmin(SendCloudOrderAdminMixin, OrderAdmin):
    pass

{% if cookiecutter.products_model == 'commodity' %}
__all__ = ['commodity', 'customer']
{%- else %}
admin.site.register(Manufacturer, admin.ModelAdmin)

__all__ = ['customer']

    {%- if cookiecutter.products_model == 'smartcard' %}


@admin.register(SmartCard)
class SmartCardAdmin(SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} CMSPageAsCategoryMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['product_name', 'slug', 'product_code', 'unit_price', 'active'{% if cookiecutter.use_i18n != 'y' %}, 'caption', 'description'{% endif %}],
        }),
        {%- if cookiecutter.use_i18n == 'y' %}
        (_("Translatable Fields"), {
            'fields': ['caption', 'description'],
        }),
        {%- endif %}
        (_("Properties"), {
            'fields': ['manufacturer', 'storage', 'card_type'],
        }),
    ]
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ['product_name']}
    list_display = ['product_name', 'product_code', 'unit_price', 'active']
    search_fields = ['product_name']

    {%- elif cookiecutter.products_model == 'polymorphic' %}

@admin.register(Commodity)
class CommodityAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} FrontendEditableAdminMixin,
                     PlaceholderAdminMixin, CMSPageAsCategoryMixin, admin.ModelAdmin):
    """
    Since our Commodity model inherits from polymorphic Product, we have to redefine its admin class.
    """
    base_model = Product
    fields = ['product_name', 'slug', 'product_code', 'unit_price', 'active', 'caption', 'manufacturer']
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ['product_name']}


@admin.register(SmartCard)
class SmartCardAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} FrontendEditableAdminMixin,
                     CMSPageAsCategoryMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
    base_model = Product
    fieldsets = (
        (None, {
            'fields': ['product_name', 'slug', 'product_code', 'unit_price', 'active'{% if cookiecutter.use_i18n != 'y' %}, 'caption', 'description'{% endif %}],
        }),
        {%- if cookiecutter.use_i18n  == 'y' %}
        (_("Translatable Fields"), {
            'fields': ['caption', 'description'],
        }),
        {%- endif %}
        (_("Properties"), {
            'fields': ['manufacturer', 'storage', 'card_type', 'speed'],
        }),
    )
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ['product_name']}


admin.site.register(OperatingSystem, admin.ModelAdmin)


class SmartPhoneInline(admin.TabularInline):
    model = SmartPhoneVariant
    extra = 0


@admin.register(SmartPhoneModel)
class SmartPhoneAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} FrontendEditableAdminMixin,
                      CMSPageAsCategoryMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
    base_model = Product
    fieldsets = [
        (None, {
            'fields': ['product_name', 'slug', 'active'{% if cookiecutter.use_i18n != 'y' %}, 'caption', 'description'{% endif %}],
        }),
    {%- if cookiecutter.use_i18n == 'y' %}
        (_("Translatable Fields"), {
            'fields': ['caption', 'description'],
        }),
    {%- endif %}
        (_("Properties"), {
            'fields': ['manufacturer', 'battery_type', 'battery_capacity', 'ram_storage',
                       'wifi_connectivity', 'bluetooth', 'gps', 'operating_system',
                       ('width', 'height', 'weight',), 'screen_size'],
        }),
    ]
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline, SmartPhoneInline]
    prepopulated_fields = {'slug': ['product_name']}

    def save_model(self, request, obj, form, change):
        if not change:
            # since SortableAdminMixin is missing on this class, ordering has to be computed by hand
            max_order = self.base_model.objects.aggregate(max_order=Max('order'))['max_order']
            obj.order = max_order + 1 if max_order else 1
        super(SmartPhoneAdmin, self).save_model(request, obj, form, change)

    def render_text_index(self, instance):
        template = get_template('search/indexes/{{ cookiecutter.app_name }}/commodity_text.txt')
        return template.render(Context({'object': instance}))
    render_text_index.short_description = _("Text Index")


@admin.register(Product)
class ProductAdmin(PolymorphicSortableAdminMixin, PolymorphicParentModelAdmin):
    base_model = Product
    child_models = [SmartPhoneModel, SmartCard, Commodity]
    list_display = ['product_name', 'get_price', 'product_type', 'active']
    list_display_links = ['product_name']
    search_fields = ['product_name']
    list_filter = [PolymorphicChildModelFilter, CMSPageFilter]
    list_per_page = 250
    list_max_show_all = 1000

    def get_price(self, obj):
        return str(obj.get_real_instance().get_price(None))

    get_price.short_description = _("Price starting at")

    {%- endif %}
{% endif -%}
