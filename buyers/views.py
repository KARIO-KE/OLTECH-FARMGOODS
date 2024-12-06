from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Cart, Checkout, Product
from .forms import CartForm, CheckoutForm
from accounts.forms import CustomUserCreationForm
from django.urls import reverse
from .forms import LoginForm ,SignupForm
# SignUp View
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

# Cart View
def cart(request):
    cart_items = Cart.objects.filter(buyer=request.user)
    return render(request, 'buyers/cart.html', {'cart_items': cart_items})

# Add to Cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(buyer=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('buyers:cart')

# Checkout View
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.buyer = request.user
            checkout.total_amount = sum([item.product.price * item.quantity for item in Cart.objects.filter(buyer=request.user)])
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
