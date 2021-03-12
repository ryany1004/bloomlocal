import csv
import io
import json
import traceback

import django
import shopify
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from bloom.shop.models import Shop, Product
from bloom.users.models import UserRole, ShopifyShop
from bloom.users.shopify import save_shopify_product
from bloom.utils.shopping import insert_products_to_gmc, update_products_to_gmc, delete_products_to_gmc, \
    convert_to_product_data


class HomePage(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_type == UserRole.BUSINESS:
            return render(request, 'pages/business_dashboard.html', {"page": 'dashboard'})

        return render(request, 'pages/home.html', {'page': 'home'})


class ProductsPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'pages/business/products.html', {"page": 'products'})


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


class ImportProductsShopifyView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "pages/business/products-import.html")


@method_decorator(csrf_exempt, name='dispatch')
class ImportProductsFileView(View):

    def get(self, request, *args, **kwargs):
        products = '[]'
        has_data = False
        if 'products' in request.session:
            products = request.session['products']
            has_data = True
            del request.session['products']
        return render(request, "pages/business/products-file-import.html", context={'products': products, 'has_data': has_data})

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        decoded_file = file.read().decode('utf-8')
        rows = csv.reader(io.StringIO(decoded_file), delimiter=',')
        next(rows)
        products = convert_to_product_data(rows)

        return JsonResponse(data=products, safe=False)


class ImportProductsWordpressView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "pages/business/products-wordpress-import.html")


class ThirdPartyProductUpoadView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "pages/business/products-upload.html")

    def post(self, request, *args, **kwargs):
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


class SpreadsheetCallback(View):

    def get(self, request, *args, **kwargs):
        from google_auth_oauthlib.flow import Flow
        from googleapiclient.discovery import build

        code = request.GET.get('code')
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        redirect_uri = request.build_absolute_uri(reverse('shop:spreadsheet-callback'))
        credentials_path = str(settings.ROOT_DIR / settings.SPREADSHEET_CREDENTIALS)
        flow = Flow.from_client_secrets_file(
            credentials_path, SCOPES, redirect_uri=redirect_uri
        )
        try:
            flow.fetch_token(code=code)
        except:
            return HttpResponseBadRequest("invalid grant permission")

        session = flow.authorized_session()
        creds = flow.credentials

        service = build('sheets', 'v4', credentials=creds)
        # The ID and range of a sample spreadsheet.
        sheet_id = request.session['sheet_id']
        range_name = 'Sheet1!A2:M'
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=range_name).execute()
        rows = result.get('values', [])
        products = []
        if not rows:
            print('No data found.')
        else:
            products = convert_to_product_data(rows)

        del request.session['sheet_id']
        request.session['products'] = json.dumps(products)
        return redirect(reverse("shop:file-import-products"))


@method_decorator(csrf_exempt, name='dispatch')
class CustomersRedactView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print(data)
        except:
            print(traceback.format_exc())
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ShopRedactView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            shop_domain = data['shop_domain']
            ShopifyShop.objects.filter(shop_url__icontains=shop_domain).delete()
        except:
            print(traceback.format_exc())
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CustomersDataRequestView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print(data)
        except:
            print(traceback.format_exc())
        return HttpResponse(status=200)
