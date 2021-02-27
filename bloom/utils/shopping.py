import json
import os
import urllib

from django.core.files.base import File
from django.db import models
from django.db.models.expressions import Value, F
from django.db.models.functions import Concat

from bloom.shop.models import Product, ImageStorage, ProductImage, ProductVariant

contentLanguage = 'en'
targetCountry = "CA"

def get_product_data(product, domain):
    offer_id = '{}'.format(product.id)
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
            product.thumbnail.url if product.thumbnail else None,
        'contentLanguage':
            contentLanguage,
        'targetCountry':
            targetCountry,
        'channel':
            'online',
        'availability':
            'in stock',
        'condition':
            'new',
        'identifier_exists': 'no',
        #'gtin': product.gtin,
        'mpn': product.mpn,
        'brand': product.brand,
        'price': {
            'value': product.price,
            'currency': 'CAD'
        },
        'shipping': [{
            'country': targetCountry,
            'service': 'Standard shipping'
        }],
    }
    if product.weight:
        p['shippingWeight'] = {
            'value': product.weight,
            'unit': product.weight_unit
        }

    if product.length:
        p['shippingLength'] = {
            'value': product.length,
            'unit': product.dimension_unit
        }

    if product.width:
        p['shippingWidth'] = {
            'value': product.width,
            'unit': product.dimension_unit
        }

    if product.height:
        p['shippingHeight'] = {
            'value': product.height,
            'unit': product.dimension_unit
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
                    product_ids.append(product['offerId'])
                elif errors:
                    print('Errors for batch entry %d:' % entry['batchId'])
                    print(json.dumps(errors, sort_keys=True, indent=2,
                                     separators=(',', ': ')))

            new_content_id = Concat(
                Value('online:'),
                Value(contentLanguage),
                Value(":"),
                Value(targetCountry),
                Value(":"),
                'id',
                output_field=models.CharField()
            )
            products = Product.objects.filter(id__in=product_ids) \
                .update(content_product_id=new_content_id)
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
                    product_ids.append(product['offerId'])
                    new_content_id = Concat(
                        Value('online:'),
                        Value(contentLanguage),
                        Value(":"),
                        Value(targetCountry),
                        Value(":"),
                        'id',
                        output_field=models.CharField()
                    )
                    Product.objects.filter(id__in=product_ids) \
                        .update(content_product_id=new_content_id)
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
                    product_ids.append(batch['entries'][entry['batchId']]['productId'].split(":")[-1])

            Product.objects.filter(id__in=product_ids).update(content_product_id="")

        else:
            print('There was an error. Response: %s' % result)
    else:
        print("**************** No any product to delete **********************")


def save_product_data(p, data):
    p.title = data['title']
    p.description = data['description'].strip()
    p.price = data['price']
    p.stock = data['stock']
    p.status = data['status']
    p.enable_color = data['enable_color']
    p.enable_size = data['enable_size']

    for field in ['length', 'width', 'height', 'dimension_unit', 'weight', 'weight_unit']:
        if field in data:
            setattr(p, field, data[field])

    if data['thumbnail']:
        result = urllib.request.urlretrieve(data['thumbnail'])
        p.thumbnail.save(os.path.basename(data['thumbnail'].split("?")[0]), File(open(result[0], 'rb')))
    p.save()

    images = []
    count = 1
    for img in data['images']:
        temp = ImageStorage()
        result = urllib.request.urlretrieve(img['src'])
        filename = os.path.basename(img['src'].split("?")[0])
        temp.image.save(filename, File(open(result[0], 'rb')))
        images.append({'url': str(temp.image), 'name': filename, 'uid': count})
        count += 1

    if images:
        product_img = ProductImage.objects.get_or_create(product=p)[0]
        product_img.images = images
        product_img.save()

    if data['variants']:
        variant = ProductVariant.objects.get_or_create(product=p)[0]
        variant.values = data['variants']
        variant.save()


def get_variant(row, enable_color, enable_size):
    variant = None
    price = float(row[4]) if isdigit(row[4]) else 0
    if row[2] and enable_color and row[3] and enable_size:
        variant = {'color': row[2], 'size': row[3], 'price': price}
    elif row[2] and enable_color:
        variant = {'color': row[2], 'price': price}
    elif row[3] and enable_size:
        variant = {'size': row[3], 'price': price}
    return variant


def isdigit(s):
    """ Returns True is string is a number. """
    if s is None:
        return False
    return s.replace('.', '', 1).isdigit()


def convert_to_product_data(rows):
    products = []
    title = None
    variants = []
    images = []
    product = None
    for row in rows:
        if row[0] != "" and row[0] != title:
            if product:
                product['variants'] = variants
                product['images'] = images
                products.append(product)

            title = row[0]
            enable_color = True if row[2] else False
            enable_size = True if row[3] else False
            variants = []
            variant = get_variant(row, enable_color, enable_size)
            if variant:
                variants.append(variant)

            images = [{'src': row[5]}] if row[5] else []
            product = {
                'title': row[0],
                'description': row[1].strip(),
                'price': float(row[4]) if isdigit(row[4]) else 0,
                'enable_color': enable_color,
                'enable_size': enable_size,
                'status': 0 if row[12] == 'active' else 1,
                'variants': variants,
                'thumbnail': row[5] if row[5] else None,
                'images': images,
                'categories': [],
                'stock': 0,
                'length': float(row[6]) if isdigit(row[6]) else None,
                'width': float(row[7]) if isdigit(row[7]) else None,
                'height': float(row[8]) if isdigit(row[8]) else None,
                'dimension_unit': row[9] if row[9] else '',
                'weight': float(row[10]) if isdigit(row[10]) else None,
                'weight_unit': row[11] if row[11] else '',
            }
        else:
            if row[5]:
                images.append({'src': row[5]})
                product['images'] = images

            variant = get_variant(row, product['enable_color'], product['enable_size'])
            if variant:
                variants.append(variant)
                product['variants'] = variants

    if product:
        products.append(product)

    return products
