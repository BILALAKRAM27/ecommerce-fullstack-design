from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Seller, Category, CategoryAttribute, AttributeOption, Brand, 
    Product, ProductImage, ProductAttributeValue, ProductReview
)

# ========== SELLER ADMIN ==========

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'shop_name', 'rating', 'created_at', 'image_preview')
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'shop_name')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'email', 'shop_name', 'shop_description')
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Metrics', {
            'fields': ('rating',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="data:image/jpeg;base64,{}" style="max-width: 50px; max-height: 50px; border-radius: 5px;" />',
                obj.get_image_base64()
            )
        return "No image"
    image_preview.short_description = 'Profile Image'

# ========== CATEGORY ADMIN ==========

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'description')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}

@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'input_type', 'is_required', 'unit')
    list_filter = ('category', 'input_type', 'is_required')
    search_fields = ('name', 'category__name')

@admin.register(AttributeOption)
class AttributeOptionAdmin(admin.ModelAdmin):
    list_display = ('value', 'attribute')
    list_filter = ('attribute__category',)
    search_fields = ('value', 'attribute__name')

# ========== BRAND ADMIN ==========

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_url')
    search_fields = ('name',)

# ========== PRODUCT ADMIN ==========

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image_url', 'is_thumbnail')

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    fields = ('attribute', 'value')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'brand', 'base_price', 'final_price', 'stock', 'condition', 'rating_avg', 'created_at')
    list_filter = ('category', 'brand', 'condition', 'created_at', 'seller')
    search_fields = ('name', 'description', 'seller__name', 'category__name', 'brand__name')
    readonly_fields = ('created_at',)
    inlines = [ProductImageInline, ProductAttributeValueInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('seller', 'name', 'description', 'category', 'brand')
        }),
        ('Pricing', {
            'fields': ('base_price', 'discount_percentage', 'final_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'condition')
        }),
        ('Metrics', {
            'fields': ('rating_avg',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('seller', 'category', 'brand')

# ========== PRODUCT IMAGE ADMIN ==========

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_thumbnail')
    list_filter = ('is_thumbnail', 'product__category')
    search_fields = ('product__name',)

# ========== PRODUCT ATTRIBUTE VALUE ADMIN ==========

@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    list_filter = ('attribute__category', 'attribute__input_type')
    search_fields = ('product__name', 'attribute__name', 'value')

# ========== PRODUCT REVIEW ADMIN ==========

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'product__category')
    search_fields = ('buyer__name', 'product__name', 'comment')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Review Information', {
            'fields': ('buyer', 'product', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('buyer', 'product')
