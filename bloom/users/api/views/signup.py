from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.core.mail import send_mail

from bloom.utils.mails import send_email
from ..serializers import ShopperSignUpSerializer, BusinessSignUpSerializer

User = get_user_model()

class ShopperSignUpAPIView(CreateAPIView):
    serializer_class = ShopperSignUpSerializer
    permission_classes = []


class VendorSignUpAPIView(CreateAPIView):
    serializer_class = BusinessSignUpSerializer
    permission_classes = []


class VendorSignUpCompleteAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        if 'register_user' in request.session:
            user_id = request.session['register_user']
            user = get_object_or_404(User, pk=user_id)

            if settings.ACCOUNT_EMAIL_VERIFICATION:
                message = render_to_string('mails/registered_business_notify.html', context={
                    'user': user,
                    'shop': user.get_shop()
                }, request=request)

                send_email(subject="New local business registered",
                           message=message,
                           from_email=settings.DEFAULT_FROM_EMAIL,
                           recipient_list=['jon@bloomlocal.org'],
                           bcc=['hongphi.math@gmail.com'])

                msg = render_to_string('mails/welcome_to_bloom.html', context={}, request=request)
                send_email(subject="Your Store is Almost Ready",
                           message=msg,
                           from_email=settings.DEFAULT_FROM_EMAIL,
                           recipient_list=[user.email])

        if 'isSignUpSteps' in request.session:
            del request.session['isSignUpSteps']
        if 'register_user' in request.session:
            del request.session['register_user']
        return Response(status=status.HTTP_200_OK)


class SignUpInitialAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        request.session['role'] = request.GET.get('role')
        return Response(status=status.HTTP_200_OK)
