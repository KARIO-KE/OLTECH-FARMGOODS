from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser
from .forms import UserSettingsForm
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ProfilePhotoForm
from accounts.models import UserProfile
from farmers.models import Farmer
from .models import Farmer


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't commit yet, we need to handle approval
            user.is_approved = True  # Automatically approve the user upon registration
            user.save()  # Save the user first

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
                return redirect('accounts:login')
            login(request, user)

            if user.is_farmer:
                return redirect('accounts:farmer_page')

            elif user.role == 'buyer':
                return redirect('accounts:home')

        else:

            messages.error(request, "Invalid username or password.")
            return redirect('accounts:login')  # Stay on the login page

    return render(request, 'accounts/login.html')


@login_required
def home_view(request):
    user = request.user
    farmers = Farmer.objects.all()

    submitted_message = request.session.get('submitted_message', None)

    range_values = range(1, 4)

    return render(request, 'accounts/home.html', {
        'farmers': farmers,
        'submitted_message': submitted_message,
        'range_values': range_values,

    })


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
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated!')
            return redirect('settings')  # Redirect to settings page after updating
    else:
        form = UserSettingsForm(instance=request.user)

    return render(request, 'accounts/settings.html', {'form': form})


def success_page(request):
    return render(request, 'accounts/success.html')


@login_required
def upload_success(request, product_name):
    # This view will be displayed after a successful product upload
    return render(request, 'farmers/upload_success.html')


def contact_view(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Simple validation for empty fields
        if not name or not email or not message:
            return HttpResponse("All fields are required", status=400)

        # Subject and body of the email
        subject = f"Message from {name}"  # Email subject
        body = message  # Email body/content

        # The 'From' address will be the user's email address
        from_email = email  # This is dynamically set to the user's email

        # The recipient email address (your Gmail or admin's email)
        to_email = settings.EMAIL_HOST_USER  # Default recipient (your Gmail or admin's email)

        try:
            # Create the email message
            email = EmailMessage(
                subject=subject,  # Subject of the email
                body=body,  # Body/content of the email
                from_email=from_email,  # The sender's email (the user's email)
                to=[to_email],  # Recipient's email (your email or admin email)
            )

            # Set the Reply-To header to the user's email
            email.reply_to = [from_email]

            # Send the email
            email.send(fail_silently=False)

            # Return a success page with the message
            return render(request, 'accounts/contact_success.html', {
                'name': name,
            })
        except Exception as e:
            return HttpResponse(f"Error sending email: {str(e)}", status=500)

    return render(request, 'accounts/contact.html')


def profile_success(request):
    return render(request, 'accounts/profile_success.html')


def add_photo(request):
    """Allows the user to upload, change, or delete their profile photo."""
    if request.method == 'POST':
        if request.FILES.get('photo'):  # Check if a file is being uploaded
            # Handle photo upload or change
            try:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.profile_photo = request.FILES['photo']
                user_profile.save()

                messages.success(request, 'Profile photo updated successfully!')
                return redirect('accounts:profile_success')  # Redirect to the same page to show the updated photo
            except Exception as e:
                messages.error(request, f'Error uploading or changing photo: {e}')
                return redirect('accounts:profile_success')

        elif 'delete_photo' in request.POST:  # Check if delete button was clicked
            try:
                user_profile = request.user.profile
                if user_profile.profile_photo:
                    user_profile.profile_photo.delete()  # Delete the photo
                    user_profile.save()

                    messages.success(request, 'Profile photo deleted successfully!')
                else:
                    messages.error(request, 'No photo to delete.')

                return redirect('add_photo')  # Redirect back to the photo page
            except UserProfile.DoesNotExist:
                messages.error(request, 'Profile not found.')

    return render(request, 'accounts/profile_photo.html')


def farmer_detail(request, ):
    return render(request, 'accounts/farmer_detail.html')
