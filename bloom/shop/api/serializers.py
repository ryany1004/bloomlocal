from rest_framework import serializers

from bloom.shop.models import AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['value', 'text']
