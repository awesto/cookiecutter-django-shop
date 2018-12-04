# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.conf import settings
from django.contrib.auth import get_user_model


from django.core.management import call_command
from django.test import Client
from django.utils.translation import ugettext_lazy as _

from cms.api import create_page
from .initialize_shop_demo import Command as ShopCommandBase
import json

from cmsplugin_cascade.models import CascadeElement

language=settings.LANGUAGES[0][0]
try:
    from cmsplugin_cascade.clipboard.utils import plugins_from_data
except ImportError:
    from cms.plugin_pool import plugin_pool
    from djangocms_text_ckeditor.models import Text
    from djangocms_text_ckeditor.utils import plugin_tags_to_id_list, replace_plugin_tags
    from cms.api import add_plugin

    def plugins_from_data(placeholder, parent, data):
        for plugin_type, data, children_data in data:
            plugin_class = plugin_pool.get_plugin(plugin_type)
            kwargs = dict(data)
            inlines = kwargs.pop('inlines', [])
            shared_glossary = kwargs.pop('shared_glossary', None)
            instance = add_plugin(placeholder, plugin_class, language, target=parent, **kwargs)
            if isinstance(instance, CascadeElement):
                instance.plugin_class.add_inline_elements(instance, inlines)
                instance.plugin_class.add_shared_reference(instance, shared_glossary)
             
            plugins_from_data(placeholder, instance, children_data)

            if isinstance(instance, Text):
                # we must convert the old plugin IDs into the new ones,
                # otherwise links are not displayed
                id_dict = dict(zip(
                    plugin_tags_to_id_list(instance.body),
                    (t[0] for t in instance.get_children().values_list('id'))
                ))
                instance.body = replace_plugin_tags(instance.body, id_dict)
                instance.save()

User=get_user_model()

from cms.api import constants
from cms.models import Page, Placeholder,
from cms.api import create_page, copy_plugins

class Command(ShopCommandBase):
    version = 1
    help = _("Initialize the workdir to run the base of myshop, Using the maximum django-cms API and"
             "some placeholders fixtures for some pages without image.")
#    download_url = 'http://downloads.django-shop.org/django-shop-workdir_{tutorial}-{version}.zip'
#    pwd = b'z7xv'
    tutorial = "i18n_commodity"

    def handle(self,   verbosity, *args, **options):
        self.client=Client()
        self.set_options(**options)
        self.createdb_if_not_exists()
        self.clear_compressor_cache()
        call_command('migrate')

        


        def copy_cascade_clipboard_json_to_placeholder(page,target_language, file_path ):
            parent=None
            if file_path and os.path.isfile(file_path):
                cascadeclipboard_data=json.loads(open(file_path).read())
                clipboard= Placeholder.objects.create(slot='clipboard-tmp')
                target=page.placeholders.get(slot='Main Content')
                plugins_from_data(clipboard, parent, cascadeclipboard_data['plugins'])
                copy_plugins.copy_plugins_to(
                clipboard.get_plugins(),
                to_placeholder=target,
                to_language=target_language,
                )
                return True
            else:
                return False


        def path_clipboards_shop_pages(reverseid):
            json_name=reverseid.replace('-', '_').replace('shop', 'clipboard_shop')
            json_name_full="{filename}-{lang}.json".format(filename=json_name, lang=language)
            #clipboard_file_path='{workdir}/{tutorial}/clipboards_shop_pages/{filename_full}'.format(
            #  workdir=settings.WORK_DIR, tutorial=self.tutorial , filename_full=json_name_full  )
            clipboard_file_path='{projectroot}/clipboard_initialize_shop/{filename_full}'.format(
              projectroot=settings.PROJECT_ROOT, tutorial=self.tutorial , filename_full=json_name_full  )
            return clipboard_file_path , json_name_full
                
        def create_shop_page( *args,**kwargs):
            shop_page=None
            copy_clip_msg=''
            if "reverse_id" in kwargs:
                clipboard_file_path=path_clipboards_shop_pages(kwargs['reverse_id'])
                shop_page=Page.objects.filter(reverse_id=kwargs['reverse_id'])
                
                if not shop_page.exists():
                    shop_page=create_page(*args,**kwargs)
                    path_clip, json_name_full=path_clipboards_shop_pages(kwargs['reverse_id'])
                    copy_clip=copy_cascade_clipboard_json_to_placeholder(shop_page, language, path_clip )

                    if  kwargs["reverse_id"] == "shop-home":
                        shop_page.set_as_homepage()
                    shop_page.publish('en')
                    if  copy_clip:
                        copy_clip_msg=" and with {}".format( json_name_full)
                        
                    print( "The shop page with reverse_id {}{} has been created".format(
                                                                  kwargs['reverse_id'], copy_clip_msg  ))

                return shop_page

        if not   User.objects.filter(is_superuser=True):
            user = User.objects.create_user("admin", "admin@example.com", "secret")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("-------------------------------------------")
            print("The demo superuser account has been created")

        #Per simplicity all shop pages has now reverse id
        shop_home=create_shop_page( "HOME", 'INHERIT', language, navigation_extenders="CatalogMenu",
          reverse_id='shop-home', in_navigation=True, apphook="CatalogListApp",soft_root=False,)
                 
                 
        shop_cart=create_shop_page( "Cart", 'INHERIT', language, reverse_id='shop-cart',
          in_navigation=False, soft_root=True,)
                 
        if shop_cart:
            shop_checkout=create_shop_page( "Checkout", 'INHERIT', language, reverse_id='shop-checkout',
              parent=shop_cart, in_navigation=True, soft_root=False )


        shop_personal=create_shop_page("Personal Pages", 'INHERIT', language,
              in_navigation=False, soft_root=True, published=True , reverse_id='shop-personal')
              
        if shop_personal:
            shop_order=create_shop_page( "Your Orders", 'INHERIT', language, reverse_id="shop-order",
             parent=shop_personal, in_navigation=True, soft_root=False, apphook="OrderApp")
              
            if shop_order:
                shop_order_last=create_shop_page( "Thanks for Your Order",'INHERIT', language, 
                   reverse_id="shop-order-last", parent=shop_order, in_navigation=True, soft_root=True, apphook="OrderApp")

            shop_customer_details=create_shop_page( "Your Personal Details", 'INHERIT',language,
              reverse_id="shop-customer-details", slug="personal-details", parent=shop_personal,
               in_navigation=True, soft_root=False, apphook="OrderApp")

            shop_password_change=create_shop_page( "Change Password", 'INHERIT',language,
                 reverse_id="shop-password-change",  parent=shop_personal, in_navigation=True, soft_root=False)


        shop_membership = create_shop_page( "Become a Member",'INHERIT', language, slug="membership",
          reverse_id="shop-membership", in_navigation=False, soft_root=True)

        if shop_membership:

            shop_register_customer = create_shop_page("Register Customer",'INHERIT', language, slug="register-customer",
                 reverse_id="shop-register-customer", parent=shop_membership, in_navigation=True, soft_root=False)
                 
            shop_password_reset=create_shop_page( "Reset Password", 'INHERIT', language, slug="reset-password",
                 reverse_id="shop-password-reset" , parent=shop_membership, in_navigation=True, soft_root=False, )

        shop_search_product=create_shop_page("Search", 'INHERIT', language, 
                    reverse_id='shop-search-product', in_navigation=False, soft_root=False, apphook="CatalogSearchApp")


        call_command('fix_filer_bug_965')
