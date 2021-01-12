from itertools import groupby

import shopify
from django.conf import settings


def create_session(shop_url, api_key, secret_key):
    shopify.Session.setup(api_key=api_key, secret=secret_key)
    api_version = settings.SHOPIFY_API_VERSION
    return shopify.Session(shop_url, api_version)


def create_permission_url(shop, state, redirect_uri):
    session = create_session(shop.shop_url, shop.api_key, shop.secret_key)
    return session.create_permission_url(settings.SHOPIFY_API_SCOPE, redirect_uri, state)


def get_product_variants(instance):
    product_variants = instance.get_product_variants()

    options = []
    variants = []
    if len(product_variants) > 0:
        option_size = None
        option_color = None
        if instance.enable_size:
            grouped_sizes = sorted(product_variants, key=lambda x: x['size'])
            sizes = [key for key, value in groupby(grouped_sizes, lambda x: x['size'])]
            option_size = {"name": "Size", "values": sizes}

        if instance.enable_color:
            grouped_colors = sorted(product_variants, key=lambda x: x['color'])
            colors = [key for key, value in groupby(grouped_colors, lambda x: x['color'])]
            option_color = {"name": "Color", "values": colors}

        if instance.enable_size and instance.enable_color:
            options.append(option_size)
            options.append(option_color)
        elif instance.enable_size and not instance.enable_color:
            options.append(option_size)
        elif not instance.enable_size and instance.enable_color:
            options.append(option_color)

        for variant in product_variants:
            v = shopify.Variant()
            if instance.enable_size and instance.enable_color:
                v.option1 = variant['size']
                v.option2 = variant['color']
                variants.append(v)
            elif instance.enable_size and not instance.enable_color:
                v.option1 = variant['size']
                variants.append(v)
            elif not instance.enable_size and instance.enable_color:
                v.option1 = variant['color']
                variants.append(v)

    return variants, options


def save_shopify_product(product, instance, mapping_sizes, mapping_colors):
    product.title = instance.title
    product.body_html = instance.description
    product.price = instance.price
    product.handle = instance.slug
    product.status = "active" if instance.status == 0 else "draft"

    product_images = instance.get_product_images()
    product.images = [{"src": instance.thumbnail.url}] + [{
        'src': "{}{}".format(settings.MEDIA_URL, img['url'])
    } for img in product_images]

    variants, options = get_product_variants(instance)
    if variants:
        product.variants = variants
    if options:
        product.options = options
    product.save()

    instance.shopify_product_id = product.id
    instance.save()
