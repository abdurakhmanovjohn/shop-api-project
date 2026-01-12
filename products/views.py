from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly


class ProductViewSet(ModelViewSet):
  queryset = Product.objects.filter(is_active=True)
  serializer_class = ProductSerializer
  permission_classes = [IsAdminOrReadOnly]
