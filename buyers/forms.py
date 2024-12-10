from django import forms
from django.contrib.auth.models import User
from .models import Cart, Checkout


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['full_name', 'phone_number', 'payment_method', 'delivery_method']
