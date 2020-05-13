from cms.models.static_placeholder import StaticPlaceholder
from django.core.management.base import BaseCommand
from cmsplugin_cascade.models import CascadeClipboard
from shop.management.utils import deserialize_to_placeholder


class Command(BaseCommand):
    help = "Iterates over all files in Filer and creates an IconFont for all eligibles."

    def handle(self, verbosity, *args, **options):
        self.verbosity = verbosity
        self.create_social_icons()

    def create_social_icons(self):
        from cms.utils.i18n import get_public_languages

        default_language = get_public_languages()[0]

        try:
            clipboard = CascadeClipboard.objects.get(identifier='social-icons')
        except CascadeClipboard.DoesNotExist:
            self.stderr.write(
                "No Persisted Clipboard named 'social-icons' found.")
        else:
            static_placeholder = StaticPlaceholder.objects.create(
                code='Social Icons')
            deserialize_to_placeholder(
                static_placeholder.public, clipboard.data, default_language)
            deserialize_to_placeholder(
                static_placeholder.draft, clipboard.data, default_language)
            self.stdout.write("Added Social Icons to Static Placeholder")

    def publish_in_all_languages(self, page):
        from cms.api import copy_plugins_to_language
        from cms.utils.i18n import get_public_languages

        languages = get_public_languages()
        for language in languages[1:]:
            copy_plugins_to_language(page, languages[0], language)
        for language in languages:
            page.publish(language)
