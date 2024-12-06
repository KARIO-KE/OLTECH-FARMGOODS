# shop/urls.py

from django.urls import path
from . import views

app_name = 'shop'  # This sets the namespace for the shop app

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # Add other paths as necessary
]
