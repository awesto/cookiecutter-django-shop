from django.core.management.base import BaseCommand
from cmsplugin_cascade.icon.utils import zipfile, unzip_archive


class Command(BaseCommand):
    help = "Iterates over all files in Filer and creates an IconFont for all eligibles."

    def handle(self, verbosity, *args, **options):
        self.verbosity = verbosity
        self.assign_files_to_iconfonts()

    def assign_files_to_iconfonts(self):
        from filer.models.filemodels import File
        from cmsplugin_cascade.models import IconFont

        for file in File.objects.all():
            if file.label != 'Font Awesome':
                continue
            if self.verbosity >= 2:
                self.stdout.write(
                    "Creating Icon Font from: {}".format(file.label))
            try:
                zip_ref = zipfile.ZipFile(file.file, 'r')
            except zipfile.BadZipFile as exc:
                self.stderr.write(
                    "Unable to unpack {}: {}".format(file.label, exc))
            else:
                if not IconFont.objects.filter(zip_file=file).exists():
                    font_folder, config_data = unzip_archive(
                        file.label, zip_ref)
                    IconFont.objects.create(
                        identifier=config_data['name'],
                        config_data=config_data,
                        zip_file=file,
                        font_folder=font_folder,
                    )
                zip_ref.close()
