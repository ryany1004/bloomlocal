from django.urls import path
from . import  views
app_name = "shop"
urlpatterns = [
    path("<slug:slug>/", views.ShopDetails.as_view(), name="shop-details")
]
