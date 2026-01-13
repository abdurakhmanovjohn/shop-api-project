from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly


class ProductViewSet(ModelViewSet):
  queryset = Product.objects.filter(is_active=True)
  serializer_class = ProductSerializer
  permission_classes = [IsAdminOrReadOnly]


class ProductSearchView(ListAPIView):
  serializer_class = ProductSerializer
  permission_classes = [AllowAny]

  def get_queryset(self):
    query = self.request.query_params.get('q', '')
    return Product.objects.filter(
      is_active=True
    ).filter(
      Q(name__icontains=query) |
      Q(description__icontains=query)
    )
