import django_auto_prefetching
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.order.api.serializers import ShippingAddresSerializer, OrderSerializer
from bloom.order.cart import Cart
from bloom.order.models import Order
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


class ValidShippingAddress(APIView):
    def post(self, request, *args, **kwargs):
        data = ShippingAddresSerializer(data=request.data, context={"request": request})
        if data.is_valid():
            pass
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class OrderConfirm(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = ShippingAddresSerializer(data=request.data, context={"request": request})
        if data.is_valid():
            shipping = data.save()
            cart = Cart(request)
            user = request.user if request.user.is_authenticated else None
            order, session = cart.confirm_order(shopper=user, shipping=shipping,
                                                sms_update=request.data['sms_update'],
                                                shopper_share_info=request.data['shopper_share_info'])
            cart.clear()
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'session': {
                'id': session.id
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OrderDetailsAPI(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = []

    def get_object(self):
        return get_object_or_404(Order.objects.prefetch_related('order_items', "order_items__product") \
                                 .select_related('shopper', "shipping_address"), uuid=self.kwargs['uuid'])


class UserOrderListAPI(django_auto_prefetching.AutoPrefetchViewSetMixin, ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('order_items', 'order_items__product') \
            .select_related('shopper', 'shipping_address') \
            .filter(shopper=self.request.user).order_by('-created_at')
        return django_auto_prefetching.prefetch(queryset, self.serializer_class)
