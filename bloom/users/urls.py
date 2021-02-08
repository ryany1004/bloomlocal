from django.urls import path

from bloom.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    StripConnectView,
    StripAccountRefreshView, StripeSettingView, ShopifySettingView, ShopifyCallbackView, ShopInformation
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("details/", view=user_detail_view, name="detail"),
    path("shop/", view=ShopInformation.as_view(), name="shop"),
    path("stripe/connect/", view=StripConnectView.as_view(), name="stripe_connect"),
    path("stripe/refresh/", view=StripAccountRefreshView.as_view(), name="stripe_refresh"),
    path("stripe-integration/", view=StripeSettingView.as_view(), name="stripe-integration"),
    path("shopify-integration/", view=ShopifySettingView.as_view(), name="shopify-integration"),
    path("auth/shopify/callback/", view=ShopifyCallbackView.as_view(), name="shopify-callback"),
]
