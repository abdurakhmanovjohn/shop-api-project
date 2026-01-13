from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
  user_email = serializers.CharField(source='user.email', read_only=True)

  class Meta:
    model = Comment
    fields = (
      'id',
      # 'user',
      'user_email',
      # 'product',
      'text',
      'created_at'
    )
    read_only_fields = ('created_at')
