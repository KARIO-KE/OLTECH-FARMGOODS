from django.shortcuts import render, get_object_or_404, redirect
from farmers.models import Product
from .forms import ProductFilterForm
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from buyers.models import Cart
from django.contrib.auth.decorators import login_required


def product_list(request):
    # Fetch products that are approved
    products = Product.objects.filter(is_approved=True)  # Assuming 'is_approved' field is used

    # Get the filter query parameters from the GET request
    name_query = request.GET.get('name', '')
    category_query = request.GET.get('category', '')

    # Apply filters if provided
    if name_query:
        products = products.filter(name__icontains=name_query)
    if category_query:
        products = products.filter(category__name=category_query)

    return render(request, 'shop/product_list.html', {'products': products})


# View to display details of a single product
def product_detail(request, name):
    # Fetch a specific product
    product = get_object_or_404(Product, name=name)
    return render(request, 'shop/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    # Fetch the product by ID
    product = Product.objects.get(id=product_id)

    # Check if the user already has this product in their cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Redirect to the cart page after adding the product
    return redirect('buyers:cart')
