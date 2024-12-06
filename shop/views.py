# views.py (in your shop app)
from django.shortcuts import render
from .models import Product
from .forms import ProductFilterForm

def product_list(request):
    form = ProductFilterForm(request.GET)  # Use GET to handle the form submission in the URL

    if form.is_valid():
        # Filter the products using the form
        products = form.filter_products()
    else:
        # If form is not valid or no filter is applied, show all products
        products = Product.objects.all()

    return render(request, 'shop/product_list.html', {'form': form, 'products': products})
