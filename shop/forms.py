from django import forms
from .models import Product


class ProductFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', 'All Categories'),  # Empty value will show all products
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
        ('Grains', 'Grains'),
        ('Legumes', 'Legumes'),
        # Add more categories as needed
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Category")

    # Set default values for min_price and max_price (100 KES)
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Min Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}),
        initial=100  # Default value of 100 KES
    )

    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Max Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}),
        initial=10000  # Default value of 100 KES
    )

    def filter_products(self):
        """
        Custom method to filter products based on form data.
        """
        products = Product.objects.all()

        # Filter by category
        if self.cleaned_data.get('category'):
            products = products.filter(category=self.cleaned_data.get('category'))

        # Filter by price range
        if self.cleaned_data.get('min_price'):
            products = products.filter(price__gte=self.cleaned_data.get('min_price'))

        if self.cleaned_data.get('max_price'):
            products = products.filter(price__lte=self.cleaned_data.get('max_price'))

        return products
