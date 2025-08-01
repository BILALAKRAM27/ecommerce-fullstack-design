#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from buyer.models import Buyer, Order, GiftBoxOrder
from seller.models import Seller
from django.utils import timezone

# Check for specific order IDs mentioned by user
print("=== Checking for Specific Order IDs ===")
specific_ids = [82, 83, 84, 85, 86, 87]
for order_id in specific_ids:
    try:
        order = Order.objects.get(id=order_id)
        print(f"Order #{order_id}: ${order.total_amount} - {order.payment_status} - Buyer: {order.buyer.email}")
    except Order.DoesNotExist:
        try:
            order = GiftBoxOrder.objects.get(id=order_id)
            print(f"GiftBox Order #{order_id}: ${order.total_amount} - {order.payment_status} - Buyer: {order.buyer.email}")
        except GiftBoxOrder.DoesNotExist:
            print(f"Order #{order_id}: Not found")

print("\n=== Checking All Buyers ===")
buyers = Buyer.objects.all()
for buyer in buyers:
    print(f"\nBuyer: {buyer.email}")
    
    # Get all orders for this buyer
    regular_orders = Order.objects.filter(buyer=buyer).select_related('seller').order_by('-created_at')
    all_giftbox_orders = GiftBoxOrder.objects.filter(buyer=buyer).select_related('seller', 'campaign').order_by('-created_at')
    
    # Combine orders
    all_orders = list(regular_orders) + list(all_giftbox_orders)
    
    print(f"Total orders: {len(all_orders)}")
    
    # Calculate total spent (only paid orders)
    paid_orders = [order for order in all_orders if order.payment_status == 'paid']
    total_spent = sum(order.total_amount for order in paid_orders)
    
    print(f"Paid orders: {len(paid_orders)}")
    print(f"Total spent: ${total_spent:.2f}")
    
    # Check if this buyer has any orders with $8288.00
    for order in all_orders:
        if abs(order.total_amount - 8288.00) < 0.01:
            order_type = "Regular" if hasattr(order, 'items') else "GiftBox"
            print(f"*** FOUND $8288.00! Order #{order.id}: ${order.total_amount} ({order_type}) - {order.payment_status} ***")
    
    # Show recent orders
    print("Recent orders:")
    for order in all_orders[:5]:  # Show last 5 orders
        order_type = "Regular" if hasattr(order, 'items') else "GiftBox"
        print(f"  #{order.id}: ${order.total_amount} - {order.payment_status} - {order_type}") 