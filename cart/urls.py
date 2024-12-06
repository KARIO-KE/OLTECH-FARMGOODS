from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
