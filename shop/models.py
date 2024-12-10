from django.db import models
from django.contrib.auth.models import User
from farmers.models import Farmer
from accounts.models import CustomUser
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
        ('Grains', 'Grains'),
        ('Legumes', 'Legumes'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100)  # Default price in KES
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    farmer = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE,
                               limit_choices_to={'role': 'farmer'})
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
