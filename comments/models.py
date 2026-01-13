from django.db import models
from django.conf import settings
from products.models import Product


class Comment(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='comments'
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    related_name='comments'
  )
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.email} - {self.product.name}"
