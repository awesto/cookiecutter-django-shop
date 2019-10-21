# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from shop.modifiers.pool import cart_modifiers_pool
from shop.modifiers.defaults import DefaultCartModifier
from shop.serializers.cart import ExtraCartRow
from shop.money import Money
from shop.shipping.modifiers import ShippingModifier
{%- if cookiecutter.use_stripe == 'y' %}
from shop_stripe import modifiers
{%- endif %}
{%- if cookiecutter.products_model == 'commodity' %}
from myshop.models import Commodity
{%- endif %}


{%- if cookiecutter.products_model == 'polymorphic' %}
class PrimaryCartModifier(DefaultCartModifier):
    """
    Extended default cart modifier which handles the price for product variations
    """
    def process_cart_item(self, cart_item, request):
        variant = cart_item.product.get_product_variant(product_code=cart_item.product_code)
        cart_item.unit_price = variant.unit_price
        cart_item.line_total = cart_item.unit_price * cart_item.quantity
        # grandparent super
        return super(DefaultCartModifier, self).process_cart_item(cart_item, request)
{%- endif %}


class PostalShippingModifier(ShippingModifier):
    identifier = 'postal-shipping'

    def get_choice(self):
        return (self.identifier, _("Postal shipping"))

    def add_extra_cart_row(self, cart, request):
        if not self.is_active(cart.extra.get('shipping_modifier')) and len(cart_modifiers_pool.get_shipping_modifiers()) > 1:
            return
        # add a shipping flat fee
        amount = Money('5')
        instance = {'label': _("Shipping costs"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount

    def ship_the_goods(self, delivery):
        if not delivery.shipping_id:
            raise ValidationError("Please provide a valid Shipping ID")
        super(PostalShippingModifier, self).ship_the_goods(delivery)

{%- if cookiecutter.use_stripe == 'y' %}


class StripePaymentModifier(modifiers.StripePaymentModifier):
    commision_percentage = 3
{%- endif %}
