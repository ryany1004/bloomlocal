from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from ..serializers import ShopperSignUpSerializer, BusinessSignUpSerializer


class ShopperSignUpAPIView(CreateAPIView):
    serializer_class = ShopperSignUpSerializer
    permission_classes = []


class VendorSignUpAPIView(CreateAPIView):
    serializer_class = BusinessSignUpSerializer
    permission_classes = []


class SignUpInitialAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        request.session['role'] = request.GET.get('role')
        return Response(status=status.HTTP_200_OK)
