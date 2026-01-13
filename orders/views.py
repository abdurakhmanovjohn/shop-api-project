from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
      return Response(
        {"error": "Cart is empty"},
        status=status.HTTP_400_BAD_REQUEST
      )

    order = Order.objects.create(user=request.user)

    for item in cart.items.all():
      OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity,
        price=item.product.price
      )

    cart.items.all().delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    if request.user.is_staff:
      orders = Order.objects.all()
    else:
      orders = Order.objects.filter(user=request.user)

    serializer = OrderSerializer(
      orders,
      many=True,
      context={"request": request}
    )
    return Response(serializer.data)


class OrderDetailView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, order_id):
    if request.user.is_staff:
      order = get_object_or_404(Order, id=order_id)
    else:
      order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
      )

    serializer = OrderSerializer(order)
    return Response(serializer.data)


class OrderStatusUpdateView(APIView):
  permission_classes = [IsAuthenticated]

  def patch(self, request, order_id):
    if not request.user.is_staff:
      return Response(
        {"error": "Admin only"},
        status=status.HTTP_403_FORBIDDEN
      )

    order = get_object_or_404(Order, id=order_id)
    status_value = request.data.get("status")

    if status_value not in dict(Order.STATUS_CHOICES):
      return Response(
        {"error": "Invalid status"},
        status=status.HTTP_400_BAD_REQUEST
      )

    order.status = status_value
    order.save()
    return Response({"detail": "Status updated"})


class OrderCancelView(APIView):
  permission_classes = [IsAuthenticated]

  def delete(self, request, order_id):
    order = get_object_or_404(
      Order,
      id=order_id,
      user=request.user
    )

    if order.status == Order.STATUS_SHIPPED:
      return Response(
        {"error": "Cannot cancel shipped order"},
        status=status.HTTP_400_BAD_REQUEST
      )

    order.delete()
    return Response({"detail": "Order cancelled"})
