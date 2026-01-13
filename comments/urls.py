from django.urls import path
from .views import (
  ProductCommentsView,
  CommentDetailView,
  MyCommentsView,
)

urlpatterns = [
  path(
    "products/<int:product_id>/comments/",
    ProductCommentsView.as_view()
  ),
  path(
    "comments/<int:comment_id>/",
    CommentDetailView.as_view()
  ),
  path(
    "products/comments/",
    MyCommentsView.as_view()
  ),
]
