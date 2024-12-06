from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

DEFAULT_PRICE = 100.00  # You can adjust this value as needed

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100, default='100')  # Fixed indentation here
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=DEFAULT_PRICE)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    def __str__(self):
        return self.name

