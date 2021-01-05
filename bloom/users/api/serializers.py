from allauth.account.utils import send_email_confirmation
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from bloom.shop.models import Shop

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "username", "email", 'first_name', 'last_name', 'phone_number', 'following_shops',
                  'love_shops', 'wishlist_products', 'stripe_account_id', 'charges_enabled']


class ShopperSignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username', 'password', 'confirm_password']
        write_only_fields = ('password',)

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.role_type = '2'
        user.save()
        if settings.ACCOUNT_EMAIL_VERIFICATION:
            send_email_confirmation(self.context['request'], user, signup=True, email=validated_data['email'])
        return user

    def validate_email(self, val):
        if User.objects.filter(email=val).exists():
            raise serializers.ValidationError("This email already exists")

        return val

    def validate_password(self, val):
        request = self.context['request']
        if (request.data.get('confirm_password') != val):
            raise serializers.ValidationError("You must type the same password each time.")

        return val


class BusinessSignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    categories = serializers.ListField(write_only=True)
    apartment = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password',
                  'business_phone', 'business_address', 'categories', 'apartment']
        write_only_fields = ('password',)

    def create(self, validated_data):
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'business_phone', 'business_address', ]
        data = {}
        for field in fields:
            data[field] = validated_data.get(field)

        user = super().create(data)
        user.set_password(validated_data['password'])
        user.role_type = '1'
        user.save()

        shop = Shop()
        shop.name = "My Shop"
        shop.owner = user
        shop.business_address = validated_data['business_address']
        shop.business_phone = validated_data['business_phone']
        shop.apartment = validated_data['apartment']
        shop.save()

        shop.categories.add(*validated_data['categories'])

        if settings.ACCOUNT_EMAIL_VERIFICATION:
            send_email_confirmation(self.context['request'], user, signup=True, email=validated_data['email'])
        return user

    def validate_email(self, val):
        if User.objects.filter(email=val).exists():
            raise serializers.ValidationError("This email already exists")

        return val

    def validate_password(self, val):
        request = self.context['request']
        if (request.data.get('confirm_password') != val):
            raise serializers.ValidationError("You must type the same password each time.")

        return val


class ShopperSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'business_phone', 'business_address',
                  'store_type', ]
