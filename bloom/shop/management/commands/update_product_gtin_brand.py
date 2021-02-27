from django.core.management.base import BaseCommand

from bloom.shop.models import Product


class Command(BaseCommand):
    help = 'Update Shop location'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for p in products.iterator():
            p.save()

        print("Done")
