import binascii
import os

import shopify
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.fields.json import JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bloom.base import BaseModelMixin


class UserRole:
    ADMIN = '0'
    BUSINESS = '1'
    SHOPPER = '2'


class User(AbstractUser):
    """Default user for Bloom."""

    #: First and last name do not cover name patterns around the globe
    ROLE_TYPES = (
        (UserRole.ADMIN, "Admin"),
        (UserRole.BUSINESS, "Local Business"),
        (UserRole.SHOPPER, "Shopper"),
    )

    # name = models.CharField(_("Name of User"), blank=True, max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    business_address = models.CharField(max_length=200, blank=True)
    business_phone = models.CharField(max_length=20, blank=True)
    locality = models.CharField(max_length=20, blank=True)
    role_type = models.CharField(max_length=10, choices=ROLE_TYPES, blank=True)
    following_shops = JSONField(default=list, blank=True)
    love_shops = JSONField(default=list, blank=True)
    wishlist_products = JSONField(default=list, blank=True)
    charges_enabled = models.BooleanField(default=False, editable=False)
    stripe_account_id = models.CharField(max_length=100, blank=True, editable=False, db_index=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.get_full_name()

    def get_charge_status(self):
        if self.charges_enabled:
            return "Connected"

        return "Unknown"

    def get_shop(self):
        from bloom.shop.models import Shop
        shop = self.shop_set.first()
        if not shop:
            shop = Shop.objects.create(owner=self, name='My Shop')
        return shop

    def get_shopify_config(self):
        return ShopifyConfig.objects.get_or_create(user=self)[0]

    def enable_shopify_import(self):
        return ShopifyConfig.objects.filter(user=self).exclude(secret_key="").exists()


class MyCollection(BaseModelMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_name = models.CharField(max_length=255, blank=True)
    products = JSONField(default=list, blank=True)

    def __str__(self):
        return self.collection_name


class FollowedShops(BaseModelMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_name = models.CharField(max_length=255, blank=True)
    shops = JSONField(default=list, blank=True)

    def __str__(self):
        return self.collection_name


class RecentViewedShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    viewed_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'shop']]


class ShopifyConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_url = models.URLField(blank=True, )
    api_key = models.CharField(max_length=200, blank=True)
    secret_key = models.CharField(max_length=200, blank=True)
    access_token = models.CharField(max_length=200, blank=True, editable=False)

    def __str__(self):
        return self.user.__str__()
