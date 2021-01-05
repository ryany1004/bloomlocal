

def get_product_data(product, domain, common):
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
