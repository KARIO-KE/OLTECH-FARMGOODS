# shop/urls.py

from django.urls import path
from . import views

app_name = 'shop'  # This sets the namespace for the shop app

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('product/<str:name>/', views.product_detail, name='product_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
]
