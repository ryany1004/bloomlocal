import json

from bloom.shop.models import Product


def get_product_data(product, domain):
    offer_id = 'product#{}'.format(product.id)
    # categories = [c.name for c in product.categories.all()]
    p = {
        'offerId':
            offer_id,
        'title':
            product.title,
        'description':
            product.description,
        'link':
            domain + product.get_absolute_url(),
        'imageLink':
            product.thumbnail.url,
        'contentLanguage':
            'en',
        'targetCountry':
            'US',
        'channel':
            'online',
        'availability':
            'in stock',
        'condition':
            'new',
        # 'googleProductCategory':
        #     ", ".join(categories),
        'price': {
            'value': product.price,
            'currency': 'USD'
        }
    }
    if product.content_product_id:
        p['id'] = product.content_product_id
    return p


def insert_products_to_gmc(products, domain, service, merchant_id):
    if products.count() > 0:
        batch = {
            'entries': [{
                'batchId': i,
                'merchantId': merchant_id,
                'method': 'insert',
                'product': get_product_data(p, domain),
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


def update_products_to_gmc(products, domain, service, merchant_id):
    if products.count() > 0:
        batch = {
            'entries': [{
                'batchId': i,
                'merchantId': merchant_id,
                'method': 'insert',
                'product': get_product_data(p, domain),
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
                    print('Product "%s" with offerId "%s" was updated.' %
                          (product['id'], product['offerId']))
                    product_ids.append(product['offerId'].split("#")[1])
                elif errors:
                    print('Errors for batch entry %d:' % entry['batchId'])
                    print(json.dumps(errors, sort_keys=True, indent=2,
                                     separators=(',', ': ')))
        else:
            print('There was an error. Response: %s' % result)
    else:
        print("**************** No any product to update **********************")


def delete_products_to_gmc(products, domain, service, merchant_id):
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
