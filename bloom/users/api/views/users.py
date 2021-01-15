import itertools

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bloom.order.api.serializers import ShippingAddressSerializer
from bloom.order.models import ShippingAddress
from bloom.shop.api.serializers import ShopSerializer, RecentViewedShopSerializer, ProductModelSerializer
from bloom.shop.models import Shop, Product
from bloom.users.api.serializers import UserSerializer, CollectionSimpleSerializer, CollectionSerializer
from bloom.users.models import RecentViewedShop, MyCollection

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class FollowingShopAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs['shop_id'] in user.following_shops:
            user.following_shops.remove(kwargs['shop_id'])
        else:
            user.following_shops.append(kwargs['shop_id'])
        user.save()

        serializer = UserSerializer(user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class WishlistProductAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        if 'id' in data['collection']:
            collection = get_object_or_404(MyCollection, id=data['collection']['id'], user=request.user)
        else:
            collection = MyCollection(collection_name=data['collection']['collection_name'],
                                      user=request.user)

        if kwargs['product_id'] in collection.products:
            collection.products.remove(kwargs['product_id'])
        else:
            collection.products.append(kwargs['product_id'])
        collection.save()

        user = request.user
        objs = MyCollection.objects.filter(user=request.user).values_list('products', flat=True)
        wishlist_products = list(set(itertools.chain.from_iterable(objs)))
        user.wishlist_products = wishlist_products
        user.save()

        data = {
            'user': UserSerializer(instance=user, context={"request": request}).data,
            'collection': CollectionSimpleSerializer(instance=collection, context={"request": request}).data
        }
        return Response(status=status.HTTP_200_OK, data=data)


class MyCollectionsAPI(ListAPIView):
    serializer_class = CollectionSimpleSerializer

    def get_serializer_class(self):
        if self.request.GET.get('simple'):
            return self.serializer_class
        return CollectionSerializer

    def get_queryset(self):
        return MyCollection.objects.filter(user=self.request.user)


class RecentViewedShopAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        shop_id = kwargs['shop_id']

        instance, created = RecentViewedShop.objects.get_or_create(user=user, shop_id=shop_id)
        if not created:
            instance.save()
        return Response(status=status.HTTP_200_OK)


class FollowedShopsListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get_queryset(self):
        shop_ids = self.request.user.following_shops;
        return Shop.objects.prefetch_related('categories').filter(id__in=shop_ids)


class RecentViewedShopsListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecentViewedShopSerializer

    def get_queryset(self):
        return RecentViewedShop.objects.filter(user=self.request.user) \
                   .prefetch_related("shop__categories").select_related('shop') \
                   .order_by('-viewed_date')[:20]


class SimilarShopsListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer

    def get_queryset(self):
        shop = self.request.user.get_shop()
        categories_ids = list(shop.categories.all().values_list('id', flat=True))
        return Shop.objects.filter(categories__in=categories_ids).prefetch_related('categories').exclude(id=shop.id)


class WishlistProductsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        return Product.objects.filter(id__in=self.request.user.wishlist_products) \
            .select_related('shop') \
            .prefetch_related('productimage_set', 'productvariant_set', 'categories')


class SavedAddressesAPI(ListCreateAPIView):
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        return ShippingAddress.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeleteSaveAddress(RetrieveDestroyAPIView):
    serializer_class = ShippingAddressSerializer
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(ShippingAddress, pk=self.kwargs['id'], owner=self.request.user)
