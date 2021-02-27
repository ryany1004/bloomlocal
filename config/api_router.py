from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter, SimpleRouter

from bloom.users.api import views
from bloom.shop.api import views as shop_views
from bloom.order.api import views as order_views
from bloom.analytics.api import views as analytics_apis

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", views.UserViewSet)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('accounts/shopper/signup/', views.ShopperSignUpAPIView.as_view(), name="shopper-signup"),
    path('accounts/vendor/signup/', views.VendorSignUpAPIView.as_view(), name="vendor-signup"),
    path('accounts/signup/initial/', views.SignUpInitialAPIView.as_view(), name="signup-initial"),
    path('product/attribute/<code>/', shop_views.AttributeValueAPIView.as_view(), name="attribute-values"),
    path('product/categories/', shop_views.CategoryAPIView.as_view(), name="product-categories"),
    path('shop/products/', shop_views.ShopProductListAPI.as_view(), name="shop-product-list"),
    path('shop/<int:shop_id>/products/', shop_views.PublishShopProductList.as_view(), name="publish-shop-product-list"),
    path('shop/product/upload/', shop_views.UploadProductAPI.as_view(), name="product-upload"),
    path('shop/product/<uuid>/', shop_views.ProductDetails.as_view(), name="product-details"),
    path('shop/product/attribute/<uuid>/', shop_views.UpdateAttributeProductAPI.as_view(), name="update-attribute-product"),
    path('shops/', shop_views.ShopListAPI.as_view(), name="shop-list"),
    path('shop/categories/', shop_views.ShopCategoryAPIView.as_view(), name="shop-categories"),
    path('shop/upload/generate-url/', shop_views.UploadURLAPI.as_view(), name="upload-url"),
    path('user/shop/<int:shop_id>/following/', views.FollowingShopAPI.as_view(), name="following-shop"),
    path('user/product/<int:product_id>/collection/', views.WishlistProductAPI.as_view(), name="wishlist-product"),
    path('user/collections/', views.MyCollectionsAPI.as_view(), name="my-collections"),
    path('user/shop/<int:shop_id>/recent-viewed/', views.RecentViewedShopAPI.as_view(), name="recent-viewed-shop"),
    path('order/cart/', order_views.CartAPI.as_view(), name="cart-data"),
    path('order/cart/item/add/', order_views.CartAddAPI.as_view(), name="cart-add"),
    path('order/cart/item/remove/', order_views.CartRemoveItemAPI.as_view(), name="cart-remove"),
    path('order/shipping-address/valid/', order_views.ValidShippingAddress.as_view(), name="valid-shipping-address"),
    path('order/confirm/', order_views.OrderConfirm.as_view(), name="order-confirm"),
    path('order/<uuid>/details/', order_views.OrderDetailsAPI.as_view(), name="order-details"),
    path('user/followed-shops/', views.FollowedShopsListAPI.as_view(), name="followed-shops"),
    path('user/recent-viewed-shops/', views.RecentViewedShopsListAPI.as_view(), name="recent-viewed-shops"),
    path('user/similar-shops/', views.SimilarShopsListAPI.as_view(), name="similar-shops"),
    path('user/wishlist-products/', views.WishlistProductsAPI.as_view(), name="wishlist-product"),
    path('user/orders/', order_views.UserOrderListAPI.as_view(), name="user-orders"),
    path('user/saved-addresses/', views.SavedAddressesAPI.as_view(), name="saved-addresses"),
    path('user/saved-address/<int:id>/', views.DeleteSaveAddress.as_view(), name="delete-saved-address"),
    path('product/search/', shop_views.ProductSearch.as_view(), name="product-search"),
    path('shop/search/', shop_views.ShopSearch.as_view(), name="shop-search"),
]

# Business API
urlpatterns += [
    path('business/my-orders/', order_views.BusinessMyOrdersAPI.as_view(), name="my-orders"),
    path('shopify/retrieve-products/', order_views.ShopifyRetrieveProductAPI.as_view(),
         name="shopify-retrieve-product"),
    path('wordpress/retrieve-products/', order_views.WordpressRetrieveProductAPI.as_view(),
         name="wordpress-retrieve-product"),
    path('shopify/import-product/', shop_views.ShopifyImportProduct.as_view(), name="shopify-import-product"),
    path('wordpress/import-product/', shop_views.WordpressImportProduct.as_view(), name="wordpress-import-product"),
    path('file/import-product/', shop_views.FileImportProductStorefront.as_view(), name="file-import-product"),
    path('spreadsheet/authorization-url/', shop_views.SpreadsheetPermissionURL.as_view(),
         name="spreadsheet-permission-url"),
    path('statistic/order-revenue/by-month/', order_views.OrderRevenueMonthAPI.as_view(), name="order-revenue-month"),
    path('statistic/order-revenue/by-year/', order_views.OrderRevenueYearAPI.as_view(), name="order-revenue-year"),
]

# Analytics API
urlpatterns += [
    path('analytics/storefront/<uuid>/', analytics_apis.StorefrontViewAPI.as_view(), name="track-storefront-view"),
    path('analytics/product/<uuid>/', analytics_apis.ProductViewAPI.as_view(), name="track-product-view"),
    path('analytics/product-view/', analytics_apis.ProductViewData.as_view(), name="product-view-report"),
    path('analytics/product-view-channels/', analytics_apis.ProductViewChannelsData.as_view(), name="product-view-channels-report"),
    path('analytics/storefront-view/', analytics_apis.StorefrontViewData.as_view(), name="storefront-view-report"),
    path('analytics/product-added-to-cart/', analytics_apis.ProductAddedToCartData.as_view(), name="product-added-to-cart-report"),
    path('analytics/shop-revenue/', analytics_apis.ShopRevenueData.as_view(), name="shop-revenue-report"),
    path('analytics/order/', analytics_apis.ShopOrderData.as_view(), name="shop-order-report"),
    path('analytics/popular-products-sale-and-view/', analytics_apis.ShopPopularProductsData.as_view(), name="shop-popular-products-report"),
    path('analytics/sale-pie-chart/', analytics_apis.SalePieChartData.as_view(), name="sale-pie-chart-report"),
    path('analytics/other-data-report/', analytics_apis.OtherDataReport.as_view(), name="other-data-report"),
]
