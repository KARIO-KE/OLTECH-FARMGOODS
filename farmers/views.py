from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.utils.text import slugify
from .forms import ProductForm, MessageForm
from .models import Product, Message  # Import Product from models
from accounts.forms import CustomUserCreationForm
from django.db import models
from .forms import UserSettingsForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import Farmer


@login_required
def farmer_home(request):
    # Check if the user is not a farmer
    if not request.user.is_farmer:
        return redirect('home')  # Redirect to home if not a farmer

    # Render the farmer page if the user is a farmer
    return render(request, 'accounts/farmer_page.html')


def about_view(request):
    return render(request, 'accounts/about.html')


@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated!')
            return redirect('settings')  # Redirect to settings page after updating
    else:
        form = UserSettingsForm(instance=request.user)

    return render(request, 'accounts/settings.html', {'form': form})


@login_required(login_url='login')
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the product
            return HttpResponse("Product uploaded successfully")
        else:
            return HttpResponse("Form is not valid")
    else:
        form = ProductForm()  # Empty form for GET request
        return render(request, 'farmers/upload_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # If the current user is not the owner of the product, redirect them to another page (optional)
    if product.owner != request.user:
        messages.error(request, "You do not have permission to edit this product.")
        return redirect(
            'farmers:product_list')  # You can change 'product_list' to whatever the view is for showing the products

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('farmers:edit_product',
                            pk=product.pk)  # Redirect to the same page to show updated product details
    else:
        form = ProductForm(instance=product)

    return render(request, 'farmers/edit_product.html', {'form': form, 'product': product})


# View for listing all products uploaded by the current farmer
def product_list(request):
    # Fetch products uploaded by the current logged-in user
    products = Product.objects.filter(owner=request.user)

    # If no products are found, display a message and a button to upload a new product
    if not products:
        messages.info(request, "You have not uploaded any products yet.")

    return render(request, 'farmers/farmer_products.html', {'products': products})


# View for deleting a specific product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Check if the logged-in user is the owner of the product
    if product.owner != request.user:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('farmers:farmer_products')  # Redirect to product list if no permission

    # Delete the product
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('farmers:farmer_productst')  # Redirect to product list after deletion

    return render(request, 'farmers/confirm_delete.html', {'product': product})


@login_required
def upload_success(request):
    # Assuming the Product model is related to the user, e.g., via a ForeignKey
    products = Product.objects.filter(user=request.user)
    return render(request, 'farmers/upload_success.html', {'products': products})


def upload_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the message to the database
            form.save()
            return redirect('farmers:success_page')  # Redirect to success page after form submission
    else:
        form = MessageForm()
    return render(request, 'farmers/farmer_form_message.html', {'form': form})


# View for editing a message
def edit_message(request, pk):
    message = Message.objects.get(pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            return redirect('farmers:success_message')
    else:
        form = MessageForm(instance=message)
    return render(request, 'farmers/farmer_form_message.html', {'form': form, 'message': message})


@login_required
def message_detail(request, farmer_name):
    farmer = get_object_or_404(Farmer, name=farmer_name)
    # Your view logic here
    return render(request, 'farmers/message_view.html', {'farmer': farmer})


def delete_message(request, pk):
    message = Message.objects.get(pk=pk)
    message.delete()
    return redirect('success_page')


@login_required
def upload_success(request, product_name=None):
    if product_name is None:
        product_name = 'Default Product'
    return render(request, 'farmers/upload_success.html', {'product_name': product_name})


def success_message_view(request):
    return render(request, 'farmers/success_message.html')


@login_required
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # You can perform simple validation here
        if not name or not email or not message:
            return HttpResponse("All fields are required", status=400)

        # Sending email
        try:
            send_mail(
                f"Message from {name}",  # Subject
                message,  # Message
                email,  # From email
                [settings.EMAIL_HOST_USER],  # To email (your Gmail address)
                fail_silently=False,
            )
            return HttpResponse("Thank you for contacting us!")
        except Exception as e:
            return HttpResponse(f"Error sending email: {str(e)}", status=500)

    return render(request, 'farmers/contact.html')


def submit_to_home(request, pk):
    # Get the product by its primary key
    product = get_object_or_404(Product, pk=pk)

    # Change the status of the product or move it to the "shop" category
    product.is_available = True  # or other logic to mark it as available
    product.save()

    # Redirect to the shop/product_list.html
    return redirect('shop:product_list')
