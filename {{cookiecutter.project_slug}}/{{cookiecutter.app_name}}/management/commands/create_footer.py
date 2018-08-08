# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from cms.api import create_page


class Command(BaseCommand):
    def handle(self, verbosity, *args, **options):
        if True:
            page = create_page("About Us", 'INHERIT', 'en', slug="about",
                               parent=None, in_navigation=False, soft_root=True,
                               reverse_id='shop-about', published=True)
            create_page("About the Company", 'INHERIT', 'en', slug="company",
                        parent=page, in_navigation=True, soft_root=False, published=True)
            create_page("Jobs", 'INHERIT', 'en', slug="jobs",
                        parent=page, in_navigation=True, soft_root=False, published=True)
            create_page("Where we are", 'INHERIT', 'en', slug="find-us",
                        parent=page, in_navigation=True, soft_root=False, published=True)

            page = create_page("Contact", 'INHERIT', 'en', slug="contact",
                               parent=None, in_navigation=False, soft_root=True,
                               reverse_id='shop-contact', published=True)
            create_page("Terms & Conditions", 'INHERIT', 'en', slug="terms-conditions",
                        parent=page, in_navigation=True, soft_root=False, published=True)
            create_page("Answered Questions", 'INHERIT', 'en', slug="faq",
                        parent=page, in_navigation=True, soft_root=False, published=True)

            page = create_page("More", 'INHERIT', 'en', slug="more",
                               parent=None, in_navigation=False, soft_root=True,
                               reverse_id='shop-more', published=True)
            create_page("How to Sell", 'INHERIT', 'en', slug="howto-sell",
                        parent=page, in_navigation=True, soft_root=False, published=True)
            create_page("How to Buy", 'INHERIT', 'en', slug="howto-buy",
                        parent=page, in_navigation=True, soft_root=False, published=True)


        if True:
            page = create_page("Personal Pages", 'INHERIT', 'en', slug="mypages",
                        parent=None, in_navigation=False, soft_root=True,
                        reverse_id='shop-personal', published=True)
            create_page("Change Password", 'INHERIT', 'en', slug="change-password",
                        reverse_id='shop-password-change', parent=page, in_navigation=True, soft_root=False, published=True)

        if True:
            page = create_page("Become a Member", 'INHERIT', 'en', slug="membership",
                        parent=None, in_navigation=False, soft_root=True,
                        reverse_id='shop-membership', published=True)
            #create_page("Register Customer", 'INHERIT', 'en', slug="register-customer",
            #            reverse_id='shop-register-customer', parent=page, in_navigation=True, soft_root=False, published=True)
            #create_page("Reset Password", 'INHERIT', 'en', slug="reset-password",
            #            reverse_id='shop-password-reset', parent=page, in_navigation=True, soft_root=False, published=True)
