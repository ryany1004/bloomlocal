from django.core.management.base import BaseCommand

from bloom.shop.models import Shop


class Command(BaseCommand):
    help = 'Update Shop location'

    def handle(self, *args, **options):
        shops = Shop.objects.exclude(business_address="")
        for shop in shops.iterator():
            print("Update shop: {}".format(shop.name))
            shop.update_location_by_address(True)
