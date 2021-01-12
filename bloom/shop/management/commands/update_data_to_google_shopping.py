import json

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q

from bloom.shop.models import Product
from bloom.utils.shopping import get_product_data, update_products_to_gmc, delete_products_to_gmc
from shopping.content import common


class Command(BaseCommand):
    help = 'Sync data to Google Content API'

    def handle(self, *args, **options):
        site = Site.objects.get_current()
        domain = "{}://{}".format('https' if settings.SECURE_SSL_REDIRECT else "http", site.domain,)

        service, config, _ = common.init([''], __doc__)
        # Get the merchant ID from merchant-info.json.
        merchant_id = config['merchantId']

        products = Product.objects.filter(status=0, archived=False).exclude(content_product_id="")

        update_products_to_gmc(products, domain, service, merchant_id)

        print("******************** Delete inactivate products ****************************")
        products = Product.objects.filter(Q(status=1) | Q(archived=True)).exclude(content_product_id="")
        delete_products_to_gmc(products, domain, service, merchant_id)
