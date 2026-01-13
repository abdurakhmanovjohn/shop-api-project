from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
  product_name = serializers.CharField(source="product.name", read_only=True)

  class Meta:
    model = OrderItem
    fields = (
      "id",
      "product",
      "product_name",
      "quantity",
      "price",
    )


class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True, read_only=True)
  user_email = serializers.SerializerMethodField()

  class Meta:
    model = Order
    fields = (
      "id",
      "user_email",
      "status",
      "items",
      "created_at",
    )

  def get_user_email(self, obj):
    request = self.context.get("request")
    if request and request.user.is_staff:
      return obj.user.email
    return None
