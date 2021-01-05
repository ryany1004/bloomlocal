from django.urls import path

from bloom.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    StripConnectView,
    StripAccountRefreshView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("details/", view=user_detail_view, name="detail"),
    path("stripe/connect/", view=StripConnectView.as_view(), name="stripe_connect"),
    path("stripe/refresh/", view=StripAccountRefreshView.as_view(), name="stripe_refresh"),
]
