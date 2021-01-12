import json
import traceback

import django
import shopify
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from bloom.shop.models import Shop, Product
from bloom.users.models import UserRole
from bloom.users.shopify import save_shopify_product
from bloom.utils.shopping import insert_products_to_gmc, update_products_to_gmc, delete_products_to_gmc


class HomePage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_type == UserRole.BUSINESS:
            return render(request, 'pages/business_dashboard.html', {"page": 'dashboard'})

        return render(request, 'pages/home.html', {'page' : 'home'})


class InventoryPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/business/products.html', {"page": 'inventory'})


class MyOrderPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/business/my_orders.html', {"page": 'my_order'})


class ProductUpload(View):
    def get(self, request, *args, **kwargs):
        shop = request.user.shop_set.first()
        if not shop:
            shop = Shop(owner=request.user, name=request.user)
            shop.save()

        return render(request, 'pages/business/product_add.html', context={'shop': shop, 'page':'upload'})


class ProductUpdate(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, uuid=kwargs['uuid'])
        shop = product.shop
        context = {
            'shop': shop,
            'page': 'update',
            'product': product,
        }
        return render(request, 'pages/business/product_update.html', context=context)


class ShopDetails(DetailView):
    template_name = 'pages/shop/shop-details.html'
    context_object_name = 'shop'

    def get_object(self, queryset=None):
        return get_object_or_404(Shop, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ShopDetails, self).get_context_data(**kwargs)
        context['page'] = 'shop_details'
        return context


class ProductDetails(DetailView):
    template_name = 'pages/shop/product-details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        context['page'] = 'product'
        return context


class MyShopsView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, "pages/account/my-shops.html", {'page': "my-shops"})


class MyPurchaseView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, "pages/account/my-purchase.html", {'page': "my-purchase"})


class MyCollectionsView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, "pages/account/my-collections.html", {'page': "my-collections"})


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        search_type = request.GET.get("type", "all")
        return render(request, "pages/search.html", {'query': query, 'search_type': search_type})


class ProductsImportView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/business/products-import.html")


class ThirdPartyProductUpoadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/business/products-upload.html")

    def post(self, request, *args, **kwargs):
        product_ids = json.loads(request.body)['product_ids']
        products = Product.objects.filter(id__in=product_ids, shop=request.user.get_shop())

        config = self.request.user.get_shopify_config()
        session = shopify.Session(config.shop_url, settings.SHOPIFY_API_VERSION, config.access_token)
        shopify.ShopifyResource.activate_session(session)
        try:
            for p in products:
                if p.shopify_product_id and shopify.Product.exists(p.shopify_product_id):
                    product = shopify.Product()
                    product.id = p.shopify_product_id
                else:
                    product = shopify.Product()
                save_shopify_product(product, p)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            shopify.ShopifyResource.clear_session()

        return render(request, "pages/business/products-upload.html")

    def put(self, request, *args, **kwargs):
        from shopping.content import common

        product_ids = json.loads(request.body)['product_ids']
        products = Product.objects.filter(id__in=product_ids, shop=request.user.get_shop())

        domain = '{}://{}'.format(request.is_secure() and "https" or "http", request.get_host())
        service, config, _ = common.init([''], __doc__)
        merchant_id = config['merchantId']

        objs = products.filter(content_product_id="", status=0, archived=False)
        insert_products_to_gmc(objs, domain, service, merchant_id)

        objs = products.filter(status=0, archived=False).exclude(content_product_id="")
        update_products_to_gmc(objs, domain, service, merchant_id)

        objs = products.filter(Q(status=1) | Q(archived=True)).exclude(content_product_id="")
        delete_products_to_gmc(objs, domain, service, merchant_id)

        return render(request, "pages/business/products-upload.html")
