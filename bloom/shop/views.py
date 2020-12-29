import django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from bloom.shop.models import Shop, Product
from bloom.users.models import UserRole


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
