from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, CartItem, Order
from .forms import OrderForm


# View to display product details and add to cart
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            quantity=1
        )
        messages.success(request, f'{product.name} added to cart!')
        return redirect('cart:product_detail')

    return render(request, 'cart/product_details.html', {'product': product})


# View to display the cart
def cart_view(request):
    cart_items = CartItem.objects.all()
    if cart_items:
        total_price = sum(item.get_total_price() for item in cart_items)
        return render(request, 'buyers/cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return render(request, 'buyers/cart.html',
                      {'empty_cart_message': 'Your cart is empty! Browse our categories and discover our best deals!'})


# View to handle checkout
def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('cart:thank_you')
    else:
        form = OrderForm()

    return render(request, 'buyers/checkout.html', {'form': form})


# Thank you page after checkout
def thank_you(request):
    return render(request, 'buyers/thank_you.html')

def home(request):
    return render(request, 'accounts/home.html')