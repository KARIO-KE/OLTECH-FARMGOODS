from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Cart, Checkout, Product
from .forms import CartForm, CheckoutForm
from accounts.forms import CustomUserCreationForm
from django.urls import reverse
from .forms import LoginForm, SignupForm
from django.http import HttpResponse
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Use SignupForm instead of CustomUserCreationForm
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST['password1'])  # Password from the form field password1
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                # Check if the user is a buyer or a farmer and redirect accordingly
                if user.is_farmer:
                    return redirect('farmers:farmer_page')  # Farmer's specific page
                else:
                    return redirect('buyers:home')  # Home for buyers
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'accounts/home.html', {'products': products})


def cart(request):
    # Get all cart items for the logged-in user
    cart_items = Cart.objects.filter(buyer=request.user)

    # Calculate the total price of all cart items
    total_price = sum(item.total_price() for item in cart_items)

    # Render the cart template with cart items and total price
    return render(request, 'buyers/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, product_id):
    # Get the cart from session
    cart = request.session.get('cart', [])

    # Remove the product from the cart by filtering out the item
    cart = [item for item in cart if item['id'] != product_id]

    # Update the session with the new cart data
    request.session['cart'] = cart
    request.session.modified = True  # Ensure session is marked as modified

    # Redirect back to the cart page
    return redirect('cart:cart')


# Checkout View
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.buyer = request.user
            checkout.total_amount = sum(
                [item.product.price * item.quantity for item in Cart.objects.filter(buyer=request.user)])
            checkout.save()
            Cart.objects.filter(buyer=request.user).delete()  # Clear cart after checkout
            messages.success(request, "Checkout successful!")
            return redirect('buyers:thank_you')
    else:
        form = CheckoutForm()
    return render(request, 'buyers/checkout.html', {'form': form})


# Thank You Page
def thank_you(request):
    return render(request, 'buyers/thank_you.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('buyers:login')
