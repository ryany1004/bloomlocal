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

        products = Product.objects.exclude(content_product_id="")
        if products.count() > 0:
            batch = {
                'entries': [{
                    'batchId': i,
                    'merchantId': merchant_id,
                    'method': 'delete',
                    'productId': p.content_product_id,
                } for i, p in enumerate(products.iterator())],
            }

            request = service.products().custombatch(body=batch)
            result = request.execute()

            product_ids = []
            if result['kind'] == 'content#productsCustomBatchResponse':
                for entry in result['entries']:
                    errors = entry.get('errors')
                    if errors:
                        print('Errors for batch entry %d:' % entry['batchId'])
                        print(json.dumps(entry['errors'], sort_keys=True, indent=2,
                                         separators=(',', ': ')))
                    else:
                        print('Deletion of product %s (batch entry %d) successful.' %
                              (batch['entries'][entry['batchId']]['productId'],
                               entry['batchId']))
                        product_ids.append(batch['entries'][entry['batchId']]['productId'].split('#')[1])

                Product.objects.filter(id__in=product_ids).update(content_product_id="")

            else:
                print('There was an error. Response: %s' % result)
        else:
            print("**************** No any product to delete **********************")

