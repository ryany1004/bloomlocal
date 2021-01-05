import json

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q

from bloom.shop.models import Product
from bloom.utils.shopping import get_product_data
from shopping.content import common


class Command(BaseCommand):
    help = 'Sync data to Google Content API'

    def handle(self, *args, **options):
        site = Site.objects.get_current()
        domain = "{}://{}".format('https' if settings.SECURE_SSL_REDIRECT else "http", site.domain,)

        service, config, _ = common.init([''], __doc__)
        # Get the merchant ID from merchant-info.json.
        merchant_id = config['merchantId']

        products = Product.objects.filter(content_product_id="", status=0, archived=False)

        if products.count() > 0:
            batch = {
                'entries': [{
                    'batchId': i,
                    'merchantId': merchant_id,
                    'method': 'insert',
                    'product': get_product_data(p, domain, common),
                } for i, p in enumerate(products.iterator())],
            }

            request = service.products().custombatch(body=batch)
            result = request.execute()
            product_ids = []
            if result['kind'] == 'content#productsCustomBatchResponse':
                entries = result['entries']
                for entry in entries:
                    product = entry.get('product')
                    errors = entry.get('errors')
                    if product:
                        print('Product "%s" with offerId "%s" was created.' %
                              (product['id'], product['offerId']))
                        product_ids.append(product['offerId'].split("#")[1])
                    elif errors:
                        print('Errors for batch entry %d:' % entry['batchId'])
                        print(json.dumps(errors, sort_keys=True, indent=2,
                                         separators=(',', ': ')))

                products = Product.objects.filter(id__in=product_ids)
                for p in products:
                    p.content_product_id = 'online:en:US:product#{}'.format(p.id)

                Product.objects.bulk_update(products, fields=['content_product_id'])
            else:
                print('There was an error. Response: %s' % result)
        else:
            print("**************** No any product to insert **********************")
