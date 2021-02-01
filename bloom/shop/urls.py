from django.urls import path
from . import views
app_name = "shop"
urlpatterns = [
    path("shop/<slug:slug>/", views.ShopDetails.as_view(), name="shop-details"),
    path("my-shops/", views.MyShopsView.as_view(), name="my-shops"),
    path("my-purchase/", views.MyPurchaseView.as_view(), name="my-purchase"),
    path("my-collections/", views.MyCollectionsView.as_view(), name="my-collections"),
    path("search/", views.SearchView.as_view(), name="search-page"),
    path("spreadsheet/callback/", views.SpreadsheetCallback.as_view(), name="spreadsheet-callback"),
    path("business/inventory/", views.InventoryPage.as_view(), name="inventory_page"),
    path("business/my-orders/", views.MyOrderPage.as_view(), name="orders_page"),
    path("business/product/upload/", views.ProductUpload.as_view(), name="product_add_page"),
    path("business/product/<uuid>/update/", views.ProductUpdate.as_view(), name="product_update_page"),
    path("business/products/shopify/import/", views.ImportProductsShopifyView.as_view(), name="shopify-import-products"),
    path("business/products/file/import/", views.ImportProductsFileView.as_view(), name="file-import-products"),
    path("business/google-merchant/upload/", views.ThirdPartyProductUpoadView.as_view(), name="google-merchant-upload"),
]
