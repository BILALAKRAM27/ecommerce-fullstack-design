from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import base64
import uuid

# ========== ENUMS ==========

class ProductCondition(models.TextChoices):
    NEW = 'new', 'New'
    USED = 'used', 'Used'
    REFURBISHED = 'refurbished', 'Refurbished'

class InputType(models.TextChoices):
    TEXT = 'text', 'Text'
    NUMBER = 'number', 'Number'
    DROPDOWN = 'dropdown', 'Dropdown'
    BOOLEAN = 'boolean', 'Boolean'

# ========== SELLER MODELS ==========

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    shop_name = models.CharField(max_length=100)
    shop_description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # Business address field
    image = models.BinaryField(blank=True, null=True, editable=True)  # Storing image as binary data (BLOB)
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.shop_name

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

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    input_type = models.CharField(max_length=20, choices=InputType.choices)
    is_required = models.BooleanField(default=False)
    unit = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class AttributeOption(models.Model):
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE, related_name='options')
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    base_price = models.FloatField()
    discount_percentage = models.FloatField(null=True, blank=True)
    final_price = models.FloatField(null=True, blank=True)
    stock = models.IntegerField()
    condition = models.CharField(max_length=20, choices=ProductCondition.choices)
    rating_avg = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    order_count = models.IntegerField(default=0)
    image = models.BinaryField(blank=True, null=True, editable=True)  # Storing image as binary data (BLOB)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    def __str__(self):
        return self.name

    @property
    def calculated_final_price(self):
        """Calculate final price based on base price and discount"""
        if self.final_price is not None:
            return self.final_price or 0
        
        # Ensure base_price is not None
        base_price = self.base_price or 0
        
        # Calculate final price if not set
        if self.discount_percentage and self.discount_percentage > 0:
            discount_amount = base_price * (self.discount_percentage / 100)
            return max(0, base_price - discount_amount)
        
        return base_price

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
    def thumbnail_image(self):
        thumb = self.images.filter(is_thumbnail=True).first()
        if thumb:
            return thumb
        return self.images.first()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.BinaryField(blank=True, null=True, editable=True)  # Store image as BLOB
    is_thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - Image"

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"

class ProductReview(models.Model):
    buyer = models.ForeignKey("buyer.Buyer", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.buyer.name} - {self.product.name} ({self.rating}/5)"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order', 'Order'),
        ('stock', 'Stock'),
        ('payment', 'Payment'),
        ('system', 'System'),
    ]
    
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.seller.shop_name} - {self.title}"

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('order_placed', 'Order Placed'),
        ('order_updated', 'Order Updated'),
        ('order_delivered', 'Order Delivered'),
        ('payment_received', 'Payment Received'),
        ('product_added', 'Product Added'),
        ('product_updated', 'Product Updated'),
        ('product_deleted', 'Product Deleted'),
        ('stock_low', 'Low Stock'),
        ('system', 'System'),
    ]
    
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_cleared = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.seller.shop_name} - {self.title}"

class Promotion(models.Model):
    PROMOTION_TYPES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Discount'),
        ('buy_one_get_one', 'Buy One Get One'),
        ('free_shipping', 'Free Shipping'),
    ]
    
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='promotions')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPES, default='percentage')
    discount_value = models.FloatField(help_text="Percentage or fixed amount based on promotion type")
    min_order_amount = models.FloatField(default=0, help_text="Minimum order amount to apply promotion")
    max_discount_amount = models.FloatField(null=True, blank=True, help_text="Maximum discount amount (for percentage discounts)")
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of times this promotion can be used")
    used_count = models.PositiveIntegerField(default=0)
    products = models.ManyToManyField(Product, blank=True, related_name='promotions')
    categories = models.ManyToManyField(Category, blank=True, related_name='promotions')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.seller.shop_name} - {self.name}"
    
    @property
    def is_valid(self):
        """Check if promotion is currently valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )
    
    def can_apply_to_product(self, product):
        """Check if promotion can be applied to a specific product"""
        # Check if product is in promotion's product list
        if self.products.exists() and product not in self.products.all():
            return False
        
        # Check if product's category is in promotion's category list
        if self.categories.exists() and product.category not in self.categories.all():
            return False
        
        return True
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if order_amount < self.min_order_amount:
            return 0
        
        if self.promotion_type == 'percentage':
            discount = order_amount * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount
        elif self.promotion_type == 'fixed':
            return min(self.discount_value, order_amount)
        else:
            return 0

class GiftBoxCampaign(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.price})"

class SellerGiftBoxParticipation(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='giftbox_participations')
    campaign = models.ForeignKey(GiftBoxCampaign, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seller', 'campaign')

    def __str__(self):
        return f"{self.seller} in {self.campaign}"
