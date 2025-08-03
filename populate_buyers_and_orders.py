#!/usr/bin/env python
"""
Script to populate MarketVibe database with Buyer Accounts and Orders
Run this script from the Django project root directory
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from buyer.models import Buyer, Order, OrderItem, GiftBoxOrder, Address, BuyerNotification
from seller.models import Seller, Product, Promotion, GiftBoxCampaign, SellerGiftBoxParticipation

def create_buyer_accounts():
    """Create 20 buyer accounts"""
    print("Creating Buyer Accounts...")
    
    # Buyer templates with realistic names
    buyer_names = [
        "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis", "David Wilson",
        "Lisa Anderson", "Robert Taylor", "Jennifer Martinez", "William Garcia", "Amanda Rodriguez",
        "James Lopez", "Michelle White", "Christopher Lee", "Jessica Hall", "Daniel Allen",
        "Ashley Young", "Matthew King", "Nicole Wright", "Joshua Green", "Stephanie Baker"
    ]
    
    buyers = []
    
    for i in range(20):
        buyer_number = i + 1
        email = f"buyer{buyer_number}@gmail.com"
        name = buyer_names[i]
        
        # Create user account
        user, created = User.objects.get_or_create(
            username=f"buyer{buyer_number}",
            defaults={
                'email': email,
                'first_name': name.split()[0],
                'last_name': name.split()[1] if len(name.split()) > 1 else ""
            }
        )
        
        if created:
            user.set_password("marketvibe27")
            user.save()
            print(f"✓ Created user: buyer{buyer_number}")
        
        # Create buyer profile
        buyer, created = Buyer.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'address': f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Elm Blvd', 'Cedar Ln'])}"
            }
        )
        
        if created:
            print(f"✓ Created buyer: {name} ({email})")
        
        buyers.append(buyer)
    
    return buyers

def create_buyer_addresses(buyers):
    """Create addresses for buyers"""
    print("\nCreating Buyer Addresses...")
    
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    streets = ["Main Street", "Oak Avenue", "Pine Road", "Elm Boulevard", "Cedar Lane", "Maple Drive", "Willow Way", "Birch Court", "Spruce Street", "Poplar Avenue"]
    
    for buyer in buyers:
        address, created = Address.objects.get_or_create(
            buyer=buyer,
            defaults={
                'street': f"{random.randint(100, 9999)} {random.choice(streets)}",
                'city': random.choice(cities),
                'zip_code': f"{random.randint(10000, 99999)}",
                'country': 'US'
            }
        )
        
        if created:
            print(f"✓ Created address for {buyer.name}")

def create_regular_orders(buyers):
    """Create regular product orders"""
    print("\nCreating Regular Product Orders...")
    
    sellers = list(Seller.objects.all())
    products = list(Product.objects.all())
    
    if not sellers or not products:
        print("❌ No sellers or products found. Please run seller and product population scripts first.")
        return []
    
    orders = []
    
    for buyer in buyers:
        for _ in range(2):  # 2 regular orders per buyer
            # Select random seller and products
            seller = random.choice(sellers)
            seller_products = seller.products.all()
            
            if not seller_products.exists():
                continue
            
            # Select 1-3 random products from this seller
            selected_products = random.sample(list(seller_products), min(3, seller_products.count()))
            
            # Calculate total amount
            total_amount = 0
            order_items = []
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.calculated_final_price
                total_amount += price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price
                })
            
            # Create order
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                total_amount=total_amount,
                payment_status='pending',
                order_type='cod',
                delivery_address=buyer.address or f"{random.randint(100, 9999)} Main St",
                expected_delivery_date=timezone.now().date() + timedelta(days=random.randint(3, 14)),
                notes=random.choice([
                    "Please deliver during business hours",
                    "Leave at front door if no one is home",
                    "Call before delivery",
                    "Ring doorbell twice",
                    ""
                ])
            )
            
            # Create order items
            for item_data in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    price_at_purchase=item_data['price'],
                    quantity=item_data['quantity']
                )
            
            orders.append(order)
            print(f"✓ Created regular order for {buyer.name}: ${total_amount:.2f} ({len(selected_products)} products)")
    
    return orders

def create_promotion_orders(buyers):
    """Create orders with promotions"""
    print("\nCreating Promotion Orders...")
    
    promotions = list(Promotion.objects.all())
    
    if not promotions:
        print("❌ No promotions found. Please run promotion population script first.")
        return []
    
    orders = []
    
    for buyer in buyers:
        for _ in range(2):  # 2 promotion orders per buyer
            # Select random promotion
            promotion = random.choice(promotions)
            seller = promotion.seller
            promotion_products = promotion.products.all()
            
            if not promotion_products.exists():
                continue
            
            # Select 1-2 products from promotion
            selected_products = random.sample(list(promotion_products), min(2, promotion_products.count()))
            
            # Calculate total with promotion discount
            subtotal = 0
            order_items = []
            
            for product in selected_products:
                quantity = random.randint(1, 2)
                base_price = product.calculated_final_price
                subtotal += base_price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': base_price
                })
            
            # Apply promotion discount
            if promotion.promotion_type == 'percentage':
                discount_amount = subtotal * (promotion.discount_value / 100)
                if promotion.max_discount_amount:
                    discount_amount = min(discount_amount, promotion.max_discount_amount)
                total_amount = subtotal - discount_amount
            else:
                total_amount = subtotal
            
            # Create order
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                status=random.choice(['pending', 'processing', 'shipped']),
                total_amount=total_amount,
                payment_status='pending',
                order_type='cod',
                promotion=promotion,
                delivery_address=buyer.address or f"{random.randint(100, 9999)} Main St",
                expected_delivery_date=timezone.now().date() + timedelta(days=random.randint(3, 14)),
                notes=f"Promotion applied: {promotion.name}"
            )
            
            # Create order items
            for item_data in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    price_at_purchase=item_data['price'],
                    quantity=item_data['quantity']
                )
            
            orders.append(order)
            print(f"✓ Created promotion order for {buyer.name}: ${total_amount:.2f} (Promotion: {promotion.name})")
    
    return orders

def create_giftbox_orders(buyers):
    """Create gift box orders"""
    print("\nCreating Gift Box Orders...")
    
    campaigns = list(GiftBoxCampaign.objects.all())
    
    if not campaigns:
        print("❌ No gift box campaigns found. Please run gift box population script first.")
        return []
    
    orders = []
    
    for buyer in buyers:
        for _ in range(1):  # 1 gift box order per buyer
            # Select random campaign
            campaign = random.choice(campaigns)
            
            # Get sellers participating in this campaign
            participating_sellers = campaign.participants.all()
            
            if not participating_sellers.exists():
                continue
            
            # Get the actual seller from the participation object
            seller_participation = random.choice(participating_sellers)
            seller = seller_participation.seller
            
            # Get some products from the seller for the gift box
            seller_products = seller.products.all()
            selected_products = random.sample(list(seller_products), min(3, seller_products.count())) if seller_products.exists() else []
            
            # Calculate total (campaign price + selected products)
            total_amount = float(campaign.price)
            if selected_products:
                for product in selected_products:
                    total_amount += product.calculated_final_price
            
            # Create gift box order
            giftbox_order = GiftBoxOrder.objects.create(
                buyer=buyer,
                seller=seller,
                campaign=campaign,
                status=random.choice(['pending', 'packed', 'shipped']),
                payment_status='pending',
                order_type='cod',
                buyer_message=random.choice([
                    "Happy Birthday!",
                    "Congratulations!",
                    "Get well soon!",
                    "Just because I care",
                    "Enjoy your gift!",
                    ""
                ]),
                delivery_address=buyer.address or f"{random.randint(100, 9999)} Main St",
                expected_delivery_date=timezone.now().date() + timedelta(days=random.randint(5, 21)),
                total_amount=total_amount,
                reveal_contents=random.choice([True, False])
            )
            
            # Add selected products to gift box
            if selected_products:
                giftbox_order.selected_products.set(selected_products)
            
            orders.append(giftbox_order)
            print(f"✓ Created gift box order for {buyer.name}: ${total_amount:.2f} (Campaign: {campaign.name})")
    
    return orders

def create_buyer_notifications(buyers):
    """Create some notifications for buyers"""
    print("\nCreating Buyer Notifications...")
    
    notification_templates = [
        {
            'type': 'order',
            'title': 'Order Update',
            'message': 'Your order has been shipped and is on its way to you!'
        },
        {
            'type': 'price',
            'title': 'Price Drop Alert',
            'message': 'A product in your wishlist has dropped in price!'
        },
        {
            'type': 'stock',
            'title': 'Low Stock Alert',
            'message': 'A product you recently viewed is running low on stock.'
        },
        {
            'type': 'system',
            'title': 'Welcome to MarketVibe',
            'message': 'Thank you for joining MarketVibe! Start exploring our amazing products.'
        }
    ]
    
    for buyer in buyers:
        # Create 1-3 notifications per buyer
        for _ in range(random.randint(1, 3)):
            template = random.choice(notification_templates)
            
            notification = BuyerNotification.objects.create(
                buyer=buyer,
                type=template['type'],
                title=template['title'],
                message=template['message'],
                is_read=random.choice([True, False])
            )
            
            print(f"✓ Created notification for {buyer.name}: {template['title']}")

def validate_data_integrity():
    """Validate that all data is properly created"""
    print("\n🔍 Validating Data Integrity...")
    
    # Check buyers
    buyer_count = Buyer.objects.count()
    print(f"✓ Buyer Accounts: {buyer_count}")
    
    # Check orders
    regular_orders = Order.objects.count()
    giftbox_orders = GiftBoxOrder.objects.count()
    total_orders = regular_orders + giftbox_orders
    print(f"✓ Regular Orders: {regular_orders}")
    print(f"✓ Gift Box Orders: {giftbox_orders}")
    print(f"✓ Total Orders: {total_orders}")
    
    # Check order items
    order_items = OrderItem.objects.count()
    print(f"✓ Order Items: {order_items}")
    
    # Check addresses
    addresses = Address.objects.count()
    print(f"✓ Buyer Addresses: {addresses}")
    
    # Check notifications
    notifications = BuyerNotification.objects.count()
    print(f"✓ Buyer Notifications: {notifications}")
    
    # Validate relationships
    print("\n📋 Detailed Validation:")
    
    # Check orders per buyer
    for buyer in Buyer.objects.all()[:5]:
        regular_count = buyer.order_set.count()
        giftbox_count = buyer.giftbox_orders.count()
        notification_count = buyer.notifications.count()
        print(f"   • {buyer.name}: {regular_count} regular orders, {giftbox_count} gift box orders, {notification_count} notifications")
    
    # Check orders with promotions
    orders_with_promotions = Order.objects.filter(promotion__isnull=False).count()
    print(f"   • Orders with Promotions: {orders_with_promotions}")
    
    # Check COD orders
    cod_orders = Order.objects.filter(order_type='cod').count()
    cod_giftbox = GiftBoxOrder.objects.filter(order_type='cod').count()
    print(f"   • COD Orders: {cod_orders} regular + {cod_giftbox} gift box = {cod_orders + cod_giftbox}")

def main():
    """Main function to populate buyers and orders"""
    print("Starting to populate Buyer Accounts and Orders...")
    print("=" * 70)
    
    # Check prerequisites
    if not Seller.objects.exists():
        print("❌ No sellers found. Please run seller population script first.")
        return
    
    if not Product.objects.exists():
        print("❌ No products found. Please run product population script first.")
        return
    
    # Create buyer accounts
    buyers = create_buyer_accounts()
    
    # Create buyer addresses
    create_buyer_addresses(buyers)
    
    # Create regular orders
    regular_orders = create_regular_orders(buyers)
    
    # Create promotion orders
    promotion_orders = create_promotion_orders(buyers)
    
    # Create gift box orders
    giftbox_orders = create_giftbox_orders(buyers)
    
    # Create notifications
    create_buyer_notifications(buyers)
    
    # Validate data integrity
    validate_data_integrity()
    
    print("\n" + "=" * 70)
    print("✅ Buyer Accounts and Orders populated successfully!")
    print("=" * 70)
    
    # Print final summary
    print("\n📈 Final Summary:")
    print(f"   • Buyer Accounts: {Buyer.objects.count()}")
    print(f"   • Regular Orders: {Order.objects.count()}")
    print(f"   • Gift Box Orders: {GiftBoxOrder.objects.count()}")
    print(f"   • Order Items: {OrderItem.objects.count()}")
    print(f"   • Buyer Addresses: {Address.objects.count()}")
    print(f"   • Buyer Notifications: {BuyerNotification.objects.count()}")
    
    # Print sample data
    print("\n👤 Sample Buyer Accounts:")
    for buyer in Buyer.objects.all()[:5]:
        orders_count = buyer.order_set.count()
        giftbox_count = buyer.giftbox_orders.count()
        print(f"   • {buyer.name} ({buyer.email}): {orders_count} orders, {giftbox_count} gift boxes")
    
    print("\n📦 Sample Orders:")
    for order in Order.objects.all()[:5]:
        items_count = order.items.count()
        print(f"   • {order.order_number}: ${order.total_amount:.2f} ({items_count} items) - {order.status}")
    
    print("\n🎁 Sample Gift Box Orders:")
    for gb_order in GiftBoxOrder.objects.all()[:5]:
        products_count = gb_order.selected_products.count()
        print(f"   • {gb_order.order_number}: ${gb_order.total_amount:.2f} ({products_count} products) - {gb_order.status}")

if __name__ == "__main__":
    main() 