from django.db import models
from django.conf import settings  # Import settings to reference the custom user model


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100,
                                choices=[('fruits', 'Fruits'), ('vegetables', 'Vegetables'), ('grains', 'Grains')])
    image = models.ImageField(upload_to='product/', null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use AUTH_USER_MODEL
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.buyer.username} with {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def delivery_fee(self):
        return self.total_price * 0.20  # 20% delivery fee


class Checkout(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use AUTH_USER_MODEL
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=100,
                                      choices=[('mpesa', 'Mpesa'), ('bank', 'Bank'), ('paypal', 'Paypal')])
    delivery_method = models.CharField(max_length=100,
                                       choices=[('pickup', 'Pickup Station'), ('delivery', 'Home Delivery')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Checkout for {self.buyer.username}"
