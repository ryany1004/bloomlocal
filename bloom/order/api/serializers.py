from rest_framework import serializers

from bloom.order.models import ShippingAddress, Order, OrderItem
from bloom.shop.api.serializers import ProductModelSimpleSerializer
from bloom.users.api.serializers import ShopperSerializer


class ShippingAddresSerializer(serializers.Serializer):
    country = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    street_address = serializers.CharField()
    street_address_2 = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    email = serializers.EmailField()
    confirm_email = serializers.EmailField(write_only=True)
    phone_number = serializers.CharField()

    def validate_confirm_email(self, val):
        request = self.context['request']
        if request.data.get('email') != val:
            raise serializers.ValidationError("You must type the same email each time.")

        return val

    def create(self, validated_data):
        shipping = ShippingAddress()
        shipping.country = validated_data['country']
        shipping.first_name = validated_data['first_name']
        shipping.last_name = validated_data['last_name']
        shipping.city = validated_data['city']
        shipping.state = validated_data['state']
        shipping.zip_code = validated_data['zip_code']
        shipping.email = validated_data['email']
        shipping.street_address = validated_data['street_address']
        shipping.street_address_2 = validated_data['street_address_2']
        shipping.phone_number = validated_data['phone_number']
        shipping.save()
        return shipping


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductModelSimpleSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price' ,'color', 'size', 'quantity', 'commission_rate']


class OrderSerializer(serializers.ModelSerializer):
    shopper = ShopperSerializer(read_only=True)
    shipping_address = ShippingAddresSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'uuid', 'tax', 'total_price', 'shopper', 'shipping_address', 'shopper_share_info',
                  'shopper_sms_update', 'order_items']
        depth = 1
