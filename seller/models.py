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
