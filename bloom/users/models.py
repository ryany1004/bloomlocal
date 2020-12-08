from django.contrib.auth.models import AbstractUser
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

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.get_full_name()


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
