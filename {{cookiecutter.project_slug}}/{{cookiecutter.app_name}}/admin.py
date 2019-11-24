# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
{%- if cookiecutter.products_model == 'polymorphic' %}
from django.template.context import Context
from django.template.loader import get_template
    {%- if cookiecutter.stock_management == 'inventory' %}
from django.core.urlresolvers import reverse
from django.utils.html import format_html
    {%- endif %}
{%- endif %}
from django.utils.translation import ugettext_lazy as _
{%- if cookiecutter.use_i18n == 'y' %}
from parler.admin import TranslatableAdmin
{%- endif %}
from filer.models import ThumbnailOption
{%- if cookiecutter.products_model in ['commodity', 'polymorphic'] %}
from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin
{%- endif %}
from shop.admin.defaults import customer
from shop.admin.defaults.order import OrderAdmin
from shop.models.defaults.order import Order
{%- if cookiecutter.printable_invoice == 'y' %}
from shop.admin.order import PrintInvoiceAdminMixin
{%- endif %}
{%- if cookiecutter.delivery_handling in ['partial', 'common'] %}
from shop.admin.delivery import DeliveryOrderAdminMixin
{%- endif %}
{%- if cookiecutter.use_sendcloud == 'y' %}
from shop_sendcloud.admin import SendCloudOrderAdminMixin
{%- endif %}
{%- if cookiecutter.products_model == 'commodity' %}
from shop.admin.defaults import commodity
{%- elif cookiecutter.products_model in ['smartcard', 'polymorphic'] %}
from adminsortable2.admin import SortableAdminMixin{% if cookiecutter.products_model == 'polymorphic' %}, PolymorphicSortableAdminMixin{% endif %}
from shop.admin.product import CMSPageAsCategoryMixin, UnitPriceMixin, ProductImageInline, InvalidateProductCacheMixin{% if cookiecutter.products_model == 'polymorphic' %}, CMSPageFilter{% endif %}
    {%- if cookiecutter.products_model == 'polymorphic' %}
from polymorphic.admin import (PolymorphicParentModelAdmin, PolymorphicChildModelAdmin,
                               PolymorphicChildModelFilter)
from {{ cookiecutter.app_name }}.models import Product, Commodity, SmartPhoneVariant, SmartPhoneModel, OperatingSystem
    {%- endif %}
from {{ cookiecutter.app_name }}.models import Manufacturer, SmartCard
    {%- if cookiecutter.stock_management == 'inventory' %}
from {{ cookiecutter.app_name }}.models import CommodityInventory, SmartCardInventory, SmartPhoneInventory
    {%- endif %}
{% endif %}

admin.site.site_header = "{{ cookiecutter.project_name }} Administration"
admin.site.unregister(ThumbnailOption)


@admin.register(Order)
class OrderAdmin({% if cookiecutter.printable_invoice == 'y' %}PrintInvoiceAdminMixin, {% endif %}{% if cookiecutter.use_sendcloud == 'y' %}SendCloudOrderAdminMixin, {% endif %}{% if cookiecutter.delivery_handling in ['partial', 'common'] %}DeliveryOrderAdminMixin, {% endif %}OrderAdmin):
    pass

{% if cookiecutter.products_model == 'commodity' %}
__all__ = ['commodity', 'customer']
{%- else %}
admin.site.register(Manufacturer, admin.ModelAdmin)

__all__ = ['customer']

    {%- if cookiecutter.products_model == 'smartcard' %}


@admin.register(SmartCard)
class SmartCardAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} CMSPageAsCategoryMixin, UnitPriceMixin, {% if cookiecutter.products_model == 'polymorphic' %}PolymorphicChildModelAdmin{% else %}admin.ModelAdmin{% endif %}):
    fieldsets = [
        (None, {
            'fields': [
                ('product_name', 'slug'),
                ('product_code', 'unit_price'),
        {%- if cookiecutter.stock_management == 'simple' %}
                'quantity',
        {%- endif %}
                'active',
        {%- if cookiecutter.use_i18n != 'y' %}
                'caption',
                'description',
        {%- endif %}
            ],
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
    list_display = ['product_name', 'product_code', 'get_unit_price', 'active']
    search_fields = ['product_name']

    {%- elif cookiecutter.products_model == 'polymorphic' %}
        {%- if cookiecutter.stock_management == 'inventory' %}


class CommodityInventoryAdmin(admin.StackedInline):
    model = CommodityInventory
    extra = 0


class SmartCardInventoryAdmin(admin.StackedInline):
    model = SmartCardInventory
    extra = 0

        {%- endif %}


@admin.register(Commodity)
class CommodityAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} FrontendEditableAdminMixin,
                     PlaceholderAdminMixin, CMSPageAsCategoryMixin, PolymorphicChildModelAdmin):
    """
    Since our Commodity model inherits from polymorphic Product, we have to redefine its admin class.
    """
    base_model = Product
    fields = [
        ('product_name', 'slug'),
        ('product_code', 'unit_price'),
        {%- if cookiecutter.stock_management == 'simple' %}
        'quantity',
        {%- endif %}
        'active',
        'caption',
        'manufacturer',
    ]
    filter_horizontal = ['cms_pages']
    inlines = [ProductImageInline{% if cookiecutter.stock_management == 'inventory' %}, CommodityInventoryAdmin{% endif %}]
    prepopulated_fields = {'slug': ['product_name']}


@admin.register(SmartCard)
class SmartCardAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} FrontendEditableAdminMixin,
                     CMSPageAsCategoryMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
    base_model = Product
    fieldsets = (
        (None, {
            'fields': [
                ('product_name', 'slug'),
                ('product_code', 'unit_price'),
        {%- if cookiecutter.stock_management == 'simple' %}
                'quantity',
        {%- endif %}
                'active',
        {%- if cookiecutter.use_i18n != 'y' %}
                'caption',
                'description',
        {%- endif %}
            ],
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
    inlines = [ProductImageInline{% if cookiecutter.stock_management == 'inventory' %}, SmartCardInventoryAdmin{% endif %}]
    prepopulated_fields = {'slug': ['product_name']}


admin.site.register(OperatingSystem, admin.ModelAdmin)


class SmartPhoneInline(admin.TabularInline):
    model = SmartPhoneVariant
    extra = 0

    {%- if cookiecutter.stock_management == 'inventory' %}

    class Media:
        js = ['shop/js/admin/popup.js']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(SmartPhoneInline, self).get_readonly_fields(request, obj))
        readonly_fields.append('variant_admin')
        return readonly_fields

    def variant_admin(self, obj):
        link = reverse('admin:myshop_smartphonevariant_change', args=(obj.id,)), _("Edit Variant")
        return format_html(
            '<span class="object-tools"><a href="#" onclick="shopShowAdminPopup(\'{0}\', \'Edit Variant\');" class="viewsitelink">{1}</a></span>',
            *link)
    variant_admin.short_display = _("Edit Variant")

    {%- endif %}

@admin.register(SmartPhoneModel)
class SmartPhoneAdmin(InvalidateProductCacheMixin, SortableAdminMixin,{% if cookiecutter.use_i18n == 'y' %} TranslatableAdmin,{% endif %} FrontendEditableAdminMixin,
                      CMSPageAsCategoryMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
    base_model = Product
    fieldsets = [
        (None, {
            'fields': [
                ('product_name', 'slug'),
                'active',
    {%- if cookiecutter.use_i18n != 'y' %}
                'caption',
                'description',
    {%- endif %}
            ],
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

    def render_text_index(self, instance):
        template = get_template('search/indexes/{{ cookiecutter.app_name }}/commodity_text.txt')
        return template.render(Context({'object': instance}))
    render_text_index.short_description = _("Text Index")

    {%- if cookiecutter.stock_management == 'inventory' %}


class SmartPhoneInventoryAdmin(admin.StackedInline):
    model = SmartPhoneInventory


@admin.register(SmartPhoneVariant)
class SmartPhoneVariantAdmin(admin.ModelAdmin):
    inlines = [SmartPhoneInventoryAdmin]
    exclude = ['product']

    def has_module_permission(self, request):
        return False

    {%- endif %}


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
