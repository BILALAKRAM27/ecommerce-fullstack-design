from django.db import models
from django.utils import timezone
import base64
import logging
from seller.models import GiftBoxCampaign, SellerGiftBoxParticipation, Product, Seller

logger = logging.getLogger(__name__)

# ========== ENUMS ==========

class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
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
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def display_name(self):
        if self.name:
            return self.name
        if hasattr(self, 'user') and self.user:
            return self.user.username
        return "Anonymous"

class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey("seller.Product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Cart(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)

    def add_product(self, product, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self, 
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def remove_product(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

    def update_quantity(self, product, quantity):
        """Update the quantity of a product in the cart"""
        try:
            if quantity <= 0:
                # If quantity is 0 or negative, remove the item
                self.remove_product(product)
                return None
            
            item, created = CartItem.objects.get_or_create(
                cart=self,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                item.quantity = quantity
                item.save()
            
            return item
        except Exception as e:
            logger.error(f"Error updating cart quantity: {str(e)}")
            raise

    def clear(self):
        self.items.all().delete()
        self.coupon_code = None
        self.save()

    def apply_coupon(self, code):
        """Apply a coupon code to the cart"""
        valid_coupons = ["MarketVibe27", "Shopping24/7"]
        if code in valid_coupons:
            self.coupon_code = code
            self.save()
            return True
        return False

    def get_discount_percentage(self):
        """Get the current discount percentage"""
        if self.coupon_code in ["MarketVibe27", "Shopping24/7"]:
            return 0.20  # 20% discount
        return 0.10  # 10% default discount

    @property
    def total_items(self):
        """Return the number of unique items in cart, not their quantities"""
        return self.items.count()

    @property
    def total_quantity(self):
        """Return the total quantity of all items in cart"""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return round(total, 2) if total is not None else 0.0

    @property
    def discount_amount(self):
        subtotal = self.subtotal or 0
        return round(subtotal * self.get_discount_percentage(), 2)

    @property
    def tax(self):
        subtotal = self.subtotal or 0
        discount_amount = self.discount_amount or 0
        return round((subtotal - discount_amount) * 0.10, 2)  # 10% tax after discount

    @property
    def total(self):
        subtotal = self.subtotal or 0
        discount_amount = self.discount_amount or 0
        tax = self.tax or 0
        return round(subtotal - discount_amount + tax, 2)

    def get_cart_data(self):
        """Get all cart data in a dictionary format"""
        return {
            'success': True,
            'cart_count': self.total_items,  # Use total_items for unique count
            'total_quantity': self.total_quantity,  # Add total quantity if needed
            'subtotal': float(self.subtotal),
            'discount_percentage': self.get_discount_percentage() * 100,
            'discount': float(self.discount_amount),
            'tax': float(self.tax),
            'total': float(self.total),
            'coupon_code': self.coupon_code
        }

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("seller.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        price = getattr(self.product, 'calculated_final_price', 0) or 0
        return price * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            self.quantity = 1
        super().save(*args, **kwargs)

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller = models.ForeignKey("seller.Seller", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount = models.FloatField()
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    order_type = models.CharField(max_length=20, choices=[('cod', 'Cash on Delivery'), ('stripe', 'Stripe')], default='cod')
    promotion = models.ForeignKey("seller.Promotion", on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.TextField()
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    
    @property
    def order_number(self):
        return f"ORD-{self.id:06d}"
    
    @property
    def is_expired(self):
        if self.expected_delivery_date:
            from django.utils import timezone
            return timezone.now().date() > self.expected_delivery_date
        return False
    
    def __str__(self):
        return f"Order #{self.id} - {self.buyer.display_name}"
    
    class Meta:
        ordering = ['-created_at']

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

class Address(models.Model):
    buyer = models.OneToOneField('Buyer', on_delete=models.CASCADE, related_name='detailed_address')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default='US')

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

class BuyerNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('stock', 'Low Stock'),
        ('price', 'Price Drop'),
        ('order', 'Order Update'),
        ('system', 'System'),
    ]
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.buyer.name} - {self.title}"

class GiftBoxOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE, related_name='giftbox_orders')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='giftbox_orders')
    campaign = models.ForeignKey(GiftBoxCampaign, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    order_type = models.CharField(max_length=20, choices=[('cod', 'Cash on Delivery'), ('stripe', 'Stripe')], default='cod')
    promotion = models.ForeignKey("seller.Promotion", on_delete=models.SET_NULL, null=True, blank=True)
    buyer_message = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    selected_products = models.ManyToManyField(Product, blank=True, related_name='giftbox_orders')
    reveal_contents = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    total_amount = models.FloatField(default=0.0)
    
    @property
    def order_number(self):
        return f"GB-{self.id:06d}"
    
    @property
    def is_expired(self):
        if self.expected_delivery_date:
            from django.utils import timezone
            return timezone.now().date() > self.expected_delivery_date
        return False
    
    @property
    def gift_box(self):
        return self.campaign

    def __str__(self):
        return f"GiftBoxOrder #{self.id} - {self.buyer} -> {self.seller}"
