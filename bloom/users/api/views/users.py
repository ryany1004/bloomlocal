from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bloom.shop.api.serializers import ShopSerializer, RecentViewedShopSerializer, ProductModelSerializer
from bloom.shop.models import Shop, Product
from bloom.users.api.serializers import UserSerializer, ShopperSignUpSerializer
from bloom.users.models import RecentViewedShop

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


class LoveShopAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs['shop_id'] in user.love_shops:
            user.love_shops.remove(kwargs['shop_id'])
        else:
            user.love_shops.append(kwargs['shop_id'])
        user.save()

        serializer = UserSerializer(user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class WishlistProductAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if kwargs['product_id'] in user.wishlist_products:
            user.wishlist_products.remove(kwargs['product_id'])
        else:
            user.wishlist_products.append(kwargs['product_id'])
        user.save()

        serializer = UserSerializer(user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


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
