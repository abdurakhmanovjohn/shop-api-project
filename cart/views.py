from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer


def get_user_cart(user):
  cart, created = Cart.objects.get_or_create(user=user)
  return cart



class CartView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    if request.user.is_staff:
      carts = Cart.objects.all()
      serializer = CartSerializer(carts, many=True)
      return Response(serializer.data)

    cart = get_user_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


class CartAddView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request.user)

    item, created = CartItem.objects.get_or_create(
      cart=cart,
      product=product
    )

    if not created:
      item.quantity += quantity
    else:
      item.quantity = quantity

    item.save()
    return Response({"detail": "Product added to cart"})


class CartUpdateView(APIView):
  permission_classes = [IsAuthenticated]

  def patch(self, request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity"))

    cart = get_user_cart(request.user)
    item = get_object_or_404(
      CartItem,
      cart=cart,
      product_id=product_id
    )

    item.quantity = quantity
    item.save()
    return Response({"detail": "Cart updated"})


class CartRemoveView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    product_id = request.data.get("product_id")

    cart = get_user_cart(request.user)
    item = get_object_or_404(
      CartItem,
      cart=cart,
      product_id=product_id
    )

    item.delete()
    return Response({"detail": "Product removed from cart"})


class CartClearView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    cart = get_user_cart(request.user)
    cart.items.all().delete()
    return Response({"detail": "Cart cleared"})
