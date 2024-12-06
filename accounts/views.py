from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser



# Sign-up view to create new users and automatically approve them
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't commit yet, we need to handle approval
            user.is_approved = True  # Automatically approve the user upon registration
            user.save()  # Save the user first

            # Display success message only after saving
            messages.success(request, "Account created successfully!")

            # Check if the user is a Farmer or a Buyer and display appropriate messages
            if user.is_farmer:
                messages.info(request, "Your account has been approved as a Farmer.")
            elif user.role == 'buyer':
                messages.info(request, "Your account has been approved as a Buyer.")

            # Redirect to the success page
            return redirect(reverse('accounts:success_page'))
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is approved
            if not user.is_approved:
                # Account is pending approval
                messages.error(request, "Your account is pending admin approval. Please wait for approval.")
                return redirect('accounts:login')  # Stay on the login page

            # Login the user
            login(request, user)

            # If user is a farmer, redirect to the farmer page
            if user.is_farmer:
                return redirect('accounts:farmer_page')  # Redirect to the farmer page

            # If user is a buyer, redirect to the home page
            elif user.role == 'buyer':
                return redirect('accounts:home')  # Redirect to the home page (buyer page)

        else:
            # If authentication fails, show error message
            messages.error(request, "Invalid username or password.")
            return redirect('accounts:login')  # Stay on the login page

    return render(request, 'accounts/login.html')

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')
@login_required
def farmer_page_view(request):
    return render(request, 'accounts/farmer_page.html')
def logout_view(request):
    logout(request)
    return redirect("accounts:logout")
def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, "Password reset email has been sent.")
            return redirect("accounts:login")
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})
def about_view(request):
    return render(request, 'accounts/about.html')
@login_required
def settings_view(request):
    return render(request, 'accounts/settings.html')
def success_page(request):
    return render(request, 'accounts/success.html')

def view_product(request, product_name):
    # Use get_object_or_404 to fetch the product by name
    product = get_object_or_404(Product, name=product_name)
    return render(request, 'farmers/upload_success.html', {'product': product})