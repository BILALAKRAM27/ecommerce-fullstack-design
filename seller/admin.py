from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Seller, Category, CategoryAttribute, AttributeOption, Brand, 
    Product, ProductImage, ProductAttributeValue, ProductReview, GiftBoxCampaign, SellerGiftBoxParticipation,
    SellerReview, ProductReviewLike, SellerReviewLike, QuoteRequest, QuoteResponse, NewsletterSubscriber
)

# ========== SELLER ADMIN ==========

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'shop_name', 'rating', 'created_at', 'image_preview')
    list_filter = ('rating', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'shop_name', 'address')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'email', 'shop_name', 'shop_description', 'address')
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

# ========== SELLER REVIEW ADMIN ==========

@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'seller')
    search_fields = ('buyer__name', 'seller__shop_name', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Review Information', {
            'fields': ('buyer', 'seller', 'rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('buyer', 'seller')

# ========== REVIEW LIKE ADMIN ==========

@admin.register(ProductReviewLike)
class ProductReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'review', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('buyer__name', 'review__product__name')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('buyer', 'review__product')

@admin.register(SellerReviewLike)
class SellerReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'review', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('buyer__name', 'review__seller__shop_name')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('buyer', 'review__seller')

admin.site.register(GiftBoxCampaign)
admin.site.register(SellerGiftBoxParticipation)

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'buyer', 'category', 'quantity', 'unit', 'urgency', 'status', 'created_at']
    list_filter = ['status', 'urgency', 'unit', 'category', 'created_at']
    search_fields = ['product_name', 'buyer__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'expires_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('buyer', 'category', 'product_name', 'description')
        }),
        ('Requirements', {
            'fields': ('quantity', 'unit', 'urgency', 'budget_range', 'delivery_deadline')
        }),
        ('Status & Timing', {
            'fields': ('status', 'created_at', 'updated_at', 'expires_at')
        }),
    )

@admin.register(QuoteResponse)
class QuoteResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'quote_request', 'seller', 'price', 'delivery_estimate', 'is_accepted', 'is_rejected', 'created_at']
    list_filter = ['is_accepted', 'is_rejected', 'created_at', 'seller']
    search_fields = ['quote_request__product_name', 'seller__shop_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Quote Information', {
            'fields': ('quote_request', 'seller')
        }),
        ('Response Details', {
            'fields': ('price', 'delivery_estimate', 'notes')
        }),
        ('Status', {
            'fields': ('is_accepted', 'is_rejected')
        }),
        ('Timing', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'is_active', 'subscribed_at', 'preferences_summary']
    list_filter = ['role', 'is_active', 'receive_product_updates', 'receive_platform_announcements', 'subscribed_at']
    search_fields = ['email', 'user__username']
    readonly_fields = ['subscribed_at', 'updated_at']
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('email', 'role', 'user')
        }),
        ('Preferences', {
            'fields': ('receive_product_updates', 'receive_platform_announcements', 'receive_seller_tools', 'receive_buyer_recommendations')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timing', {
            'fields': ('subscribed_at', 'updated_at')
        }),
    )
