from django.urls import path
from . import views
app_name = "shop"
urlpatterns = [
    path("shop/<slug:slug>/", views.ShopDetails.as_view(), name="shop-details"),
    path("my-shops/", views.MyShopsView.as_view(), name="my-shops"),
    path("my-purchase/", views.MyPurchaseView.as_view(), name="my-purchase"),
    path("my-collections/", views.MyCollectionsView.as_view(), name="my-collections"),
    path("search/", views.SearchView.as_view(), name="search-page"),
]
