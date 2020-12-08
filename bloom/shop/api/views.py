from rest_framework.generics import ListAPIView

from bloom.shop.api.serializers import AttributeValueSerializer
from bloom.shop.models import AttributeValue


class AttributeValueAPIView(ListAPIView):
    serializer_class = AttributeValueSerializer

    def get_queryset(self):
        return AttributeValue.objects.filter(attribute__attribute_code=self.kwargs['code'])
