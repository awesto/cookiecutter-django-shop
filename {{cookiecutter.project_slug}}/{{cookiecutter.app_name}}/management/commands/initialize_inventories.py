import random
from django.core.management.base import BaseCommand
from {{ cookiecutter.app_name }}.models import Commodity, CommodityInventory, SmartCard, SmartCardInventory, SmartPhoneVariant, SmartPhoneInventory


class Command(BaseCommand):
    help = "Create Inventories for all products using random values."

    def handle(self, verbosity, *args, **options):
        self.verbosity = verbosity
        for commodity in Commodity.objects.all():
            CommodityInventory.objects.create(
                product=commodity,
                quantity=random.randint(0, 15)
            )
        for smart_card in SmartCard.objects.all():
            SmartCardInventory.objects.create(
                product=smart_card,
                quantity=random.randint(0, 55)
            )
        for smart_phone in SmartPhoneVariant.objects.all():
            SmartPhoneInventory.objects.create(
                product=smart_phone,
                quantity=random.randint(0, 8)
            )
        self.stdout.write("Created inventories with random quantities.")
