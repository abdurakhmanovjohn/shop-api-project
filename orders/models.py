from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
  STATUS_PENDING = "pending"
  STATUS_PAID = "paid"
  STATUS_SHIPPED = "shipped"

  STATUS_CHOICES = (
    (STATUS_PENDING, "Pending"),
    (STATUS_PAID, "Paid"),
    (STATUS_SHIPPED, "Shipped"),
  )

  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="orders"
  )
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=STATUS_PENDING
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):
  order = models.ForeignKey(
    Order,
    related_name="items",
    on_delete=models.CASCADE
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE
  )
  quantity = models.PositiveIntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return f"{self.product.name} x {self.quantity}"
