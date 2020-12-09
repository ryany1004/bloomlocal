from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter, SimpleRouter

from bloom.users.api import views
from bloom.shop.api import views as shop_views

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
    path('product/upload/', shop_views.UploadProductAPI.as_view(), name="product-upload"),
    path('shop/products/', shop_views.ShopProductListAPI.as_view(), name="shop-product-list"),

    path('shop/upload/generate-url/', shop_views.UploadURLAPI.as_view(), name="upload-url"),
]
