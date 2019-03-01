# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from cms.apphook_pool import apphook_pool
from cms.cms_menus import SoftRootCutter
from menus.menu_pool import menu_pool
from shop.cms_apphooks import CatalogListCMSApp, CatalogSearchCMSApp, OrderApp, PasswordResetApp


class CatalogListApp(CatalogListCMSApp):
    def get_urls(self, page=None, language=None, **kwargs):
{%- if cookiecutter.products_model == 'polymorphic' %}
        from shop.search.views import CMSPageCatalogWrapper
        from shop.views.catalog import AddToCartView, ProductRetrieveView
        from {{ cookiecutter.app_name }}.filters import ManufacturerFilterSet
        from {{ cookiecutter.app_name }}.serializers import AddSmartPhoneToCartSerializer, CatalogSearchSerializer

        return [
            url(r'^$', CMSPageCatalogWrapper.as_view(
                filter_class=ManufacturerFilterSet,
                search_serializer_class=CatalogSearchSerializer,
            )),
            url(r'^(?P<slug>[\w-]+)/?$', ProductRetrieveView.as_view(
                use_modal_dialog=False,
            )),
            url(r'^(?P<slug>[\w-]+)/add-to-cart', AddToCartView.as_view()),
            url(r'^(?P<slug>[\w-]+)/add-smartphone-to-cart', AddToCartView.as_view(
                serializer_class=AddSmartPhoneToCartSerializer,
            )),
        ]
{%- else %}{% set use_lookup_field = (cookiecutter.products_model == 'commodity' and cookiecutter.use_i18n == 'y') %}
        from shop.views.catalog import AddToCartView, ProductListView, ProductRetrieveView
        from {{ cookiecutter.app_name }}.serializers import ProductDetailSerializer

        return [
            url(r'^$', ProductListView.as_view(
                redirect_to_lonely_product=True,
            )),
            url(r'^(?P<slug>[\w-]+)/?$', ProductRetrieveView.as_view(
                serializer_class=ProductDetailSerializer,
    {%- if use_lookup_field %}
                lookup_field='translations__slug'
    {%- endif %}
            )),
            url(r'^(?P<slug>[\w-]+)/add-to-cart', AddToCartView.as_view({% if use_lookup_field %}lookup_field='translations__slug'{% endif %})),
        ]
{%- endif %}

apphook_pool.register(CatalogListApp)


class CatalogSearchApp(CatalogSearchCMSApp):
    def get_urls(self, page=None, language=None, **kwargs):
        from shop.search.views import SearchView
        from {{ cookiecutter.app_name }}.serializers import ProductSearchSerializer

        return [
            url(r'^', SearchView.as_view(
                serializer_class=ProductSearchSerializer,
            )),
        ]

apphook_pool.register(CatalogSearchApp)

apphook_pool.register(OrderApp)

apphook_pool.register(PasswordResetApp)


def _deregister_menu_pool_modifier(Modifier):
    index = None
    for k, modifier_class in enumerate(menu_pool.modifiers):
        if issubclass(modifier_class, Modifier):
            index = k
    if index is not None:
        # intentionally only modifying the list
        menu_pool.modifiers.pop(index)

_deregister_menu_pool_modifier(SoftRootCutter)
