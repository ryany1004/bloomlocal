from django.urls import path
from . import views
app_name = "shop"
urlpatterns = [
    path("shop/<slug:slug>/", views.ShopDetails.as_view(), name="shop-details"),
    path("product/<slug:slug>/", views.ProductDetails.as_view(), name="product-details")
]
