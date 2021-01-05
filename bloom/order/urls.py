from django.urls import path
from . import views
app_name = "order"
urlpatterns = [
    path("order/overview/", views.OrderOverviewPage.as_view(), name="order-overview"),
    path("order/<uuid>/purchase-confirmed/", views.OrderSuccessPage.as_view(), name="order-success"),
    path("order/<uuid>/purchase-canceled/", views.OrderCanceledPage.as_view(), name="order-canceled"),
    path("order/hooks/", views.OrderHooksPage.as_view(), name="order-hooks"),
    path("account/hooks/", views.AccountHooksPage.as_view(), name="account-hooks"),
]
