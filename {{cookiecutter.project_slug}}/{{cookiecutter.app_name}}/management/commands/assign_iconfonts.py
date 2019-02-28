# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from cmsplugin_cascade.icon.utils import zipfile, unzip_archive



class Command(BaseCommand):
    help = "Iterates over all files in Filer and creates an IconFont for all eligibles."

    def handle(self, verbosity, *args, **options):
        self.verbosity = verbosity
        self.assign_files_to_iconfonts()
        self.assign_iconfonts_to_cmspages()

    def assign_files_to_iconfonts(self):
        from filer.models.filemodels import File
        from cmsplugin_cascade.models import IconFont

        for file in File.objects.all():
            if not file.label.startswith('fontello-'):
                continue
            if self.verbosity >= 2:
                self.stdout.write("Creating Icon Font from: {}".format(file.label))
            try:
                zip_ref = zipfile.ZipFile(file.file, 'r')
            except zipfile.BadZipFile as exc:
                self.stderr.write("Unable to unpack {}: {}".format(file.label, exc))
                continue
            else:
                if not IconFont.objects.filter(zip_file=file).exists():
                    font_folder, config_data = unzip_archive(file.label, zip_ref)
                    IconFont.objects.create(
                        identifier=config_data['name'],
                        config_data=config_data,
                        zip_file=file,
                        font_folder=font_folder,
                )
            finally:
                zip_ref.close()

    def assign_iconfonts_to_cmspages(self):
        from cms.models.pagemodel import Page
        from cms.utils.i18n import get_public_languages
        from cmsplugin_cascade.models import CascadePage, IconFont

        identifier = 'fontawesome'
        try:
            fontawesome = IconFont.objects.get(identifier=identifier)
        except IconFont.DoesNotExist:
            self.stderr.write("No IconFont named '{}' found to assign to CMS page.".format(identifier))
        else:
            for page in Page.objects.drafts():
                self.stdout.write("Assign IconFont '{}' to CMS page: {}".format(identifier, page.get_title()))
                CascadePage.objects.update_or_create(
                    extended_object=page,
                    defaults={'icon_font': fontawesome},
                )
                for language in get_public_languages():
                    page.publish(language)
