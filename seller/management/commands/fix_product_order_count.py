#!/usr/bin/env python
"""
Script to update each Product's order_count based on OrderItems in the database.
Run this script from the Django project root directory.
"""

import os
import django
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Product
from buyer.models import OrderItem


def main():
    print("Updating product order_count based on OrderItems...")
    # Count orders for each product
    product_order_counts = defaultdict(int)
    for item in OrderItem.objects.all():
        product_order_counts[item.product_id] += item.quantity

    updated = 0
    for product in Product.objects.all():
        new_count = product_order_counts.get(product.id, 0)
        if product.order_count != new_count:
            product.order_count = new_count
            product.save(update_fields=['order_count'])
            updated += 1
            print(f"Updated {product.name}: order_count = {new_count}")
    print(f"Done! Updated {updated} products.")

if __name__ == "__main__":
    main()