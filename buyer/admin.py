from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Buyer, Wishlist, Cart, CartItem, Order, OrderItem, Payment, GiftBoxOrder
)

# ========== BUYER ADMIN ==========

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'image_preview')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'image_preview')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
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

# ========== WISHLIST ADMIN ==========

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'created_at')
    list_filter = ('created_at', 'product__category')
    search_fields = ('buyer__name', 'product__name')
    readonly_fields = ('created_at',)

# ========== CART ADMIN ==========

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('product', 'quantity')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'created_at', 'total_items')
    list_filter = ('created_at',)
    search_fields = ('buyer__name',)
    readonly_fields = ('created_at',)
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = 'Total Items'

# ========== CART ITEM ADMIN ==========

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    list_filter = ('product__category',)
    search_fields = ('cart__buyer__name', 'product__name')

    def total_price(self, obj):
        return f"${obj.product.base_price * obj.quantity:.2f}"
    total_price.short_description = 'Total Price'

# ========== ORDER ADMIN ==========

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'price_at_purchase', 'quantity', 'total_price')
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return f"${obj.price_at_purchase * obj.quantity:.2f}"
    total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'status', 'total_amount', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'seller')
    search_fields = ('buyer__name', 'seller__name', 'delivery_address')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('buyer', 'seller', 'status', 'total_amount')
        }),
        ('Payment', {
            'fields': ('payment_status',),
            'classes': ('collapse',)
        }),
        ('Delivery', {
            'fields': ('delivery_address',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('buyer', 'seller')

# ========== ORDER ITEM ADMIN ==========

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price_at_purchase', 'quantity', 'total_price')
    list_filter = ('product__category',)
    search_fields = ('order__buyer__name', 'product__name')
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return f"${obj.price_at_purchase * obj.quantity:.2f}"
    total_price.short_description = 'Total Price'

# ========== PAYMENT ADMIN ==========

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'transaction_id', 'status', 'payment_time')
    list_filter = ('payment_method', 'status', 'payment_time')
    search_fields = ('order__buyer__name', 'transaction_id')
    readonly_fields = ('payment_time',)
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'payment_method', 'transaction_id', 'status')
        }),
        ('Timestamps', {
            'fields': ('payment_time',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__buyer')

admin.site.register(GiftBoxOrder)
