from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  is_client = models.BooleanField(default=True)
  phone_number = models.CharField(max_length=20, unique=True)
  passport_number = models.CharField(max_length=20, blank=True, null=True)
  address = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.username} ({self.phone_number})"