from django import forms
from .models import Product
from .models import Product

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'product_type', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
