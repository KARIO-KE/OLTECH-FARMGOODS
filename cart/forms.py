from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer_name', 'email', 'phone', 'payment_method', 'delivery_method']
