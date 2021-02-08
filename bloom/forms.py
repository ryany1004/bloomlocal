from django import forms

from bloom.shop.models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'logo', 'business_address', 'business_phone', 'store_type']
