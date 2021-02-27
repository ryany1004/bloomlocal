from rest_framework import serializers

from bloom.order.models import ShippingAddress, Order, OrderItem
from bloom.shop.api.serializers import ProductModelSimpleSerializer
from bloom.users.api.serializers import ShopperSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField(write_only=True)

    class Meta:
        model = ShippingAddress
        fields = ['country', 'first_name', 'last_name', 'street_address', 'street_address_2', 'city',
                  'state', 'zip_code', 'email', 'confirm_email', 'phone_number', 'id']

    def validate_confirm_email(self, val):
        request = self.context['request']
        if request.data.get('email') != val:
            raise serializers.ValidationError("You must type the same email each time.")

        return val

    def create(self, validated_data):
        shipping = ShippingAddress()
        shipping.country = validated_data['country']
        shipping.first_name = validated_data['first_name'].title()
        shipping.last_name = validated_data['last_name'].title()
        shipping.city = validated_data['city']
        shipping.state = validated_data['state']
        shipping.zip_code = validated_data['zip_code']
        shipping.email = validated_data['email']
        shipping.street_address = validated_data['street_address']
        shipping.street_address_2 = validated_data['street_address_2']
        shipping.phone_number = validated_data['phone_number']
        if 'owner' in validated_data:
            shipping.owner = validated_data['owner']
        shipping.save()
        return shipping


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductModelSimpleSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price' ,'color', 'size', 'quantity', 'commission_rate']


class OrderSerializer(serializers.ModelSerializer):
    shopper = ShopperSerializer(read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True)
    order_no = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'uuid', 'tax', 'total_price', 'shopper', 'shipping_address', 'shopper_share_info',
                  'shopper_sms_update', 'order_items', 'order_no', 'order_status']
        depth = 1

    def get_order_no(self, obj):
        return obj.get_order_no()

    def get_order_status(self, obj):
        return obj.get_status_display()


class BusinessOrderSerializer(serializers.ModelSerializer):
    shopper = ShopperSerializer(read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'uuid', 'tax', 'total_price', 'shopper', 'shipping_address', 'shopper_share_info',
                  'shopper_sms_update', 'order_items']

    def get_order_items(self, order):
        items = OrderItem.objects.filter(order=order, product__shop__owner=self.context['request'].user)
        return BusinessOrderItemSerializer(many=True, instance=items).data


class BusinessOrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    order_uuid = serializers.SerializerMethodField()
    order_no = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'color', 'size', 'quantity', 'commission_rate', 'order_id',
                  'product_title', 'order_uuid', 'order_no']

    def get_product_title(self, obj):
        return obj.product.title

    def get_order_uuid(self, obj):
        return obj.order.uuid

    def get_order_no(self, obj):
        return "{}-{}".format(obj.order.get_order_no(), obj.get_merchant_no())
