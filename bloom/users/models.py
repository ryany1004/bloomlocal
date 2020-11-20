from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Bloom."""

    #: First and last name do not cover name patterns around the globe
    ROLE_TYPES = (
        (0, "Admin"),
        (1, "Vendor"),
        (2, "Shopper"),
    )
    STORE_TYPES = (
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('electronics', 'Electronics'),
    )
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    business_address = models.CharField(max_length=200, blank=True)
    business_phone = models.CharField(max_length=20, blank=True)
    store_type = models.CharField(max_length=20, blank=True, choices=STORE_TYPES)
    role_type = models.CharField(max_length=10, choices=ROLE_TYPES, blank=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
