from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from .models import Comment
from .serializers import CommentSerializer


class ProductCommentsView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, product_id):
    comments = Comment.objects.filter(product_id=product_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

  def post(self, request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, product=product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
  permission_classes = [IsAuthenticated]

  def patch(self, request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    serializer = CommentSerializer(
      comment,
      data=request.data,
      partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

  def delete(self, request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class MyCommentsView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    if request.user.is_staff:
      comments = Comment.objects.all()
    else:
      comments = Comment.objects.filter(user=request.user)

    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
