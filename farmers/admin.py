# farmers/admin.py

from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')  # Add created_at field here
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)
