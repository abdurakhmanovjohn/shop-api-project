from django.urls import path
from .views import (
  OrderCreateView,
  OrderListView,
  OrderDetailView,
  OrderStatusUpdateView,
  OrderCancelView,
)

urlpatterns = [
  path("order/create/", OrderCreateView.as_view()),
  path("orders/", OrderListView.as_view()),
  path("orders/<int:order_id>/", OrderDetailView.as_view()),
  path("orders/<int:order_id>/status/", OrderStatusUpdateView.as_view()),
  path("orders/<int:order_id>/cancel/", OrderCancelView.as_view()),
]
