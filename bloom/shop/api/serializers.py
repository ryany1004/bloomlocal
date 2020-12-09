from rest_framework import serializers

from bloom.shop.models import AttributeValue, Category, Product, ProductVariant, ProductImage


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['value', 'text']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductModelSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'thumbnail', 'price', 'description', 'length', 'width', 'height', 'dimension_unit',
                  'weight', 'weight_unit', 'stock', 'delivery_type', 'enable_color', 'enable_size', 'shop_id',
                  'variants', 'images']

    def to_representation(self, instance):
        response = super(ProductModelSerializer, self).to_representation(instance)
        if instance.thumbnail:
            response['thumbnail'] = str(instance.thumbnail)
        return response

    def get_variants(self, obj):
        variants = obj.productvariant_set.all()
        if len(variants) > 0:
            return variants[0].values
        else:
            return []

    def get_images(self, obj):
        images = obj.productimage_set.all()
        if len(images) > 0:
            return images[0].images
        else:
            return []


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.FloatField()
    thumbnail = serializers.CharField()
    description = serializers.CharField()
    length = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()
    dimension_unit = serializers.CharField()
    weight = serializers.FloatField()
    weight_unit = serializers.CharField()
    stock = serializers.FloatField()
    delivery_type = serializers.CharField()
    enable_color = serializers.BooleanField(default=True)
    enable_size = serializers.BooleanField(default=True)
    shop = serializers.IntegerField()
    categories = serializers.ListField()
    variants = serializers.ListField()
    images = serializers.ListField()

    def create(self, validated_data):
        p = Product()
        p.title = validated_data['title']
        p.price = validated_data['price']
        p.thumbnail = validated_data['thumbnail']
        p.description = validated_data['description']
        p.length = validated_data['length']
        p.width = validated_data['width']
        p.height = validated_data['height']
        p.dimension_unit = validated_data['dimension_unit']
        p.weight = validated_data['weight']
        p.weight_unit = validated_data['weight_unit']
        p.stock = validated_data['stock']
        p.delivery_type = validated_data['delivery_type']
        p.enable_color = validated_data['enable_color']
        p.enable_size = validated_data['enable_size']
        p.shop_id = validated_data['shop']
        p.save()

        if validated_data['variants']:
            var = ProductVariant()
            var.product = p
            var.values = validated_data['variants']
            var.save()

        if validated_data['categories']:
            p.categories.add(*validated_data['categories'])

        if validated_data['images']:
            product_images = ProductImage()
            product_images.product = p
            product_images.images = validated_data['images']
            product_images.save()

        return p
