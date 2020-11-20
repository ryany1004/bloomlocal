from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class ShopperSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username', 'password', 'confirm_password']
        write_only_fields = ('password',)

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
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


class VendorSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password',
                  'business_phone', 'business_address', 'store_type',]
        write_only_fields = ('password',)

    def create(self, validated_data):
        del validated_data['confirm_password']
        validated_data['username'] = validated_data['email']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
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



