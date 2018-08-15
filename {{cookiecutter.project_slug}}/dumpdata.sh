#!/bin/sh
mkdir -p fixtures
./manage.py dumpdata --indent=2 --natural-foreign email_auth cms cmsplugin_cascade djangocms_text_ckeditor filer post_office shop {{ cookiecutter.app_name }} --exclude cmsplugin_cascade.segmentation --exclude filer.clipboard --exclude filer.clipboarditem --exclude {{ cookiecutter.app_name }}.order --exclude {{ cookiecutter.app_name }}.orderpayment --exclude {{ cookiecutter.app_name }}.orderitem --exclude {{ cookiecutter.app_name }}.cart --exclude {{ cookiecutter.app_name }}.cartitem > fixtures/myshop.json
