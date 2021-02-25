from django.contrib.gis.geos.point import Point
from rest_framework import serializers

from bloom.shop.models import Category, Product, ProductVariant, ProductImage, Shop, ShopCategory, Attribute
from bloom.users.models import RecentViewedShop


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductModelSimpleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    sales_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'uuid', 'title', 'thumbnail', 'price', 'description', 'length', 'width', 'height', 'status',
                  'weight', 'weight_unit', 'stock', 'delivery_type', 'enable_color', 'enable_size', 'shop_id',
                  'archived', 'slug', 'created_at', 'updated_at',
                  'dimension_unit', 'url', 'views_count', 'sales_count']

    def to_representation(self, instance):
        response = super(ProductModelSimpleSerializer, self).to_representation(instance)
        if instance.thumbnail:
            response['thumbnail'] = str(instance.thumbnail)
        return response

    def get_url(self, product):
        return product.get_absolute_url()

    def get_views_count(self, product):
        if hasattr(product, 'views_count'):
            return product.views_count or 0
        return 0

    def get_sales_count(self, product):
        if hasattr(product, 'sales_count'):
            return product.sales_count or 0
        return 0


class ProductModelSerializer(ProductModelSimpleSerializer):
    variants = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'uuid', 'title', 'thumbnail', 'price', 'description', 'length', 'width', 'height', 'status',
                  'weight', 'weight_unit', 'stock', 'delivery_type', 'enable_color', 'enable_size', 'shop_id',
                  'archived', 'slug', 'variants', 'images', 'created_at', 'updated_at', 'categories',
                  'category_names', 'dimension_unit', 'url']

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

    def get_category_names(self, obj):
        return [c.name for c in obj.categories.all()]

    def update(self, instance, validated_data):
        if 'description' in validated_data:
            validated_data['description'] = validated_data['description'].strip()
            print (validated_data['description'])
        return super(ProductModelSerializer, self).update(instance, validated_data)


class ProductSearchSerializer(ProductModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'uuid', 'title', 'thumbnail', 'price', 'description', 'length', 'width', 'height', 'status',
                  'weight', 'weight_unit', 'stock', 'delivery_type', 'enable_color', 'enable_size', 'shop_id',
                  'archived', 'slug', 'variants', 'images', 'created_at', 'updated_at', 'categories',
                  'category_names', 'dimension_unit', 'url', 'distance']

    def get_distance(self, obj):
        request = self.context['request']
        if 'lat' in request.GET and 'long' in request.GET and obj.shop.location:
            point = Point((float(request.GET['lat']), float(request.GET['long'])))
            return obj.shop.location.distance(point) * 100
        return None


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    price = serializers.FloatField(min_value=0)
    thumbnail = serializers.CharField(max_length=500)
    description = serializers.CharField()
    length = serializers.FloatField(min_value=0)
    width = serializers.FloatField(min_value=0)
    height = serializers.FloatField(min_value=0)
    dimension_unit = serializers.CharField()
    weight = serializers.FloatField(min_value=0)
    weight_unit = serializers.CharField()
    stock = serializers.FloatField(min_value=0)
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
        p.description = validated_data['description'].strip()
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

    def update(self, instance, validated_data):
        if "thumbnail" in validated_data:
            instance.thumbnail = validated_data['thumbnail']
            instance.save()

        if 'enable_color' in validated_data:
            instance.enable_color = validated_data['enable_color']
            instance.save()

        if 'enable_size' in validated_data:
            instance.enable_size = validated_data['enable_size']
            instance.save()

        if 'images' in validated_data:
            product_imgs = instance.productimage_set.first()
            if product_imgs:
                product_imgs.images = validated_data['images']
                product_imgs.save()

        if 'variants' in validated_data:
            product_variants = instance.productvariant_set.first()
            if product_variants:
                product_variants.values = validated_data['variants']
                product_variants.save()

        return instance


class ShopSerializer(serializers.ModelSerializer):
    category_names = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'uuid', 'name', 'slug', 'logo', 'owner', 'business_address', 'business_phone',
                  'categories', 'locality', 'category_names', 'url']

    def to_representation(self, instance):
        response = super(ShopSerializer, self).to_representation(instance)
        if instance.logo:
            response['logo'] = str(instance.logo)
        else:
            response['logo'] = "shop/7f094ea2/7f09__sample-image.jpg"
        return response

    def get_category_names(self, obj):
        return [{"name": c.name, 'id': c.id} for c in obj.categories.all()]

    def get_url(self, shop):
        return shop.get_absolute_url()


class ShopSearchSerializer(ShopSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'uuid', 'name', 'slug', 'logo', 'owner', 'business_address', 'business_phone',
                  'categories', 'locality', 'category_names', 'url', 'distance']

    def get_distance(self, shop):
        request = self.context['request']
        if 'lat' in request.GET and 'long' in request.GET and shop.location:
            point = Point((float(request.GET['lat']), float(request.GET['long'])))
            return shop.location.distance(point) * 100

        return None

class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = ['id', 'name']


class RecentViewedShopSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = RecentViewedShop
        fields = ['viewed_date', 'shop']
        depth = 1
