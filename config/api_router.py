from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from bloom.users.api import views

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
]
