# farm/views.py
from django.shortcuts import render


def main_page(request):
    return render(request, 'accounts/main.html')


def shop_view(request):
    # Your logic for the shop view
    return render(request, 'shop/product_list.html')
