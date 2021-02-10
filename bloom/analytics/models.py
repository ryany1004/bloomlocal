from django.db import models


class StorefrontView(models.Model):
    shop = models.ForeignKey("shop.Shop", on_delete=models.CASCADE)
    viewed_date = models.DateField()
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.shop.name


class ProductView(models.Model):
    CHANNEL_CHOICES = (
        ('website', "Website"),
        ('google_shop', "Google Shopping"),
    )
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    viewed_date = models.DateField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='website')
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title


class ProductAddedToCart(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    added_date = models.DateField()
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title
