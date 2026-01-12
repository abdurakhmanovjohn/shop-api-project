import random
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=150, unique=True, null=True, blank=True)
  full_name = models.CharField(max_length=255, blank=True)
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

  is_email_verified = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email


class EmailVerification(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  code = models.CharField(max_length=6)
  created_at = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    if not self.code:
      self.code = str(random.randint(100000, 999999))
    super().save(*args, **kwargs)
