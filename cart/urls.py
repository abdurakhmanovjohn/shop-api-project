from django.urls import path
from .views import (
  CartView,
  CartAddView,
  CartUpdateView,
  CartRemoveView,
  CartClearView,
)

urlpatterns = [
  path("cart/", CartView.as_view()),
  path("cart/add/", CartAddView.as_view()),
  path("cart/update/", CartUpdateView.as_view()),
  path("cart/remove/", CartRemoveView.as_view()),
  path("cart/clear/", CartClearView.as_view()),
]
