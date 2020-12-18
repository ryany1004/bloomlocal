from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter, SimpleRouter

from bloom.users.api import views
from bloom.shop.api import views as shop_views
from bloom.order.api import views as order_views

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
    path('user/shop/<int:shop_id>/love/', views.LoveShopAPI.as_view(), name="love-shop"),
    path('user/shop/<int:shop_id>/recent-viewed/', views.RecentViewdShopAPI.as_view(), name="recent-viewed-shop"),
    path('order/cart/', order_views.CartAPI.as_view(), name="cart-data"),
    path('order/cart/item/add/', order_views.CartAddAPI.as_view(), name="cart-add"),
    path('order/cart/item/remove/', order_views.CartRemoveItemAPI.as_view(), name="cart-remove"),
]
