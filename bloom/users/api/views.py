from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer, ShopperSerializer, VendorSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ShopperSignUpAPIView(CreateAPIView):
    serializer_class = ShopperSerializer
    permission_classes = []


class VendorSignUpAPIView(CreateAPIView):
    serializer_class = VendorSerializer
    permission_classes = []


class SignUpInitialAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        request.session['role'] = request.GET.get('role')
        return Response(status=status.HTTP_200_OK)
