from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductSearchView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
  path('products/search/', ProductSearchView.as_view()),
]

urlpatterns += router.urls
