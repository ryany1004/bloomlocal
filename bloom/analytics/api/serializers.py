from rest_framework import serializers

from bloom.analytics.models import StorefrontView, ProductView


class StorefrontViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorefrontView
        fields = ('id', )


class ProductViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductView
        fields = ('id', 'channel')
