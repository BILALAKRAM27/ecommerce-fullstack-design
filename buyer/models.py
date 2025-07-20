from django.db import models
from django.utils import timezone
import base64

# ========== ENUMS ==========

class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'

class PaymentMethod(models.TextChoices):
    CARD = 'card', 'Card'
    COD = 'cash_on_delivery', 'Cash on Delivery'
    STRIPE = 'stripe', 'Stripe'

# ========== BUYER MODELS ==========

class Buyer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.BinaryField(blank=True, null=True)  # Storing image as binary data (BLOB)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def set_image(self, data):
        """Set the image field as raw binary data"""
        self.image = data

    def get_image(self):
        """Get the raw binary image data"""
        return self.image

    def get_image_base64(self):
        """Returns the base64 string to display in templates"""
        if self.image:
            return base64.b64encode(self.image).decode('utf-8')
        return None

    image_data = property(get_image_base64)

class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey("seller.Product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Cart(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("seller.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller = models.ForeignKey("seller.Seller", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.FloatField()
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("seller.Product", on_delete=models.CASCADE)
    price_at_purchase = models.FloatField()
    quantity = models.PositiveIntegerField()

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices)
    payment_time = models.DateTimeField()
