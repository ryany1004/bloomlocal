from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bloom.users.api.serializers import UserSerializer, ShopperSignUpSerializer

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
