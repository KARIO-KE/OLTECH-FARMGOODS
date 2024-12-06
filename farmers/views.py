from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from accounts.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import Product, Farmer

def farmer_home(request):
    if not request.user.is_farmer:
        return redirect('home')  # Redirect to home if not a farmer
    return render(request, 'accounts/farmer_page.html')


@login_required(login_url='login')
def upload_product(request):
    # Handle POST request when the form is submitted
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        # Check if the form is valid
        if form.is_valid():
            # Extract the product name from the form data
            product_name = form.cleaned_data['name']

            # Try to find the Farmer associated with the logged-in user
            try:
                farmer = Farmer.objects.get(user=request.user)
            except Farmer.DoesNotExist:
                messages.error(request, "Upload product failed. Farmer not found.")
                return redirect('farmers:upload_product')  # Redirect back to the form

            # Create and save the product, associating it with the farmer
            product = form.save(commit=False)
            product.farmer = farmer  # Associate the product with the farmer
            product.save()

            # Show success message and redirect to a success page
            messages.success(request, f"Product '{product_name}' uploaded successfully!")
            return redirect('farmers:upload_success', product_name=product_name)

    # Handle GET request to display the empty form
    else:
        form = ProductForm()

    # Render the form for GET or when there are errors
    return render(request, 'farmers/upload_product.html', {'form': form})


@login_required
def edit_product(request):
    try:
        # Ensure the user is a farmer (add additional checks if necessary)
        farmer = request.user.farmer  # Assuming a OneToOne relationship between User and Farmer
        products = Product.objects.filter(farmer=farmer)

        # Continue with your view logic
        # For example, return the product list to the template
        return render(request, 'farmers/edit_product.html', {'products': products})

    except AttributeError:
        # Handle the case where the user does not have a related Farmer instance
        return redirect('accounts:farmer_page')  # Or handle it in another way


@login_required(login_url='login')
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id, farmer=request.user)
        product.delete()
        messages.success(request, "Product deleted successfully!")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    return redirect('edit_product')



def submit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_submitted = True
    product.save()
    return redirect('farmers:shop_view')

def view_product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'farmers/upload_success.html', {'product': product})
