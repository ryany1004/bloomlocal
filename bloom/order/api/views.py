from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.order.cart import Cart
from bloom.shop.models import Product


class CartAddAPI(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        product = get_object_or_404(Product, id=data['product_id'], status=0, archived=False)
        cart = Cart(request)
        cart.add(product, quantity=data['quantity'],size=data.get('size'), color=data.get('color'))

        return Response(data=cart.to_json(), status=status.HTTP_200_OK)


class CartRemoveItemAPI(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        product = get_object_or_404(Product, id=data['product_id'])
        cart = Cart(request)
        cart.remove(product, size=data.get('size'), color=data.get('color'))

        return Response(data=cart.to_json(), status=status.HTTP_200_OK)


class CartAPI(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return Response(cart.to_json(), status=status.HTTP_200_OK)
