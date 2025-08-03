#!/usr/bin/env python
"""
Script to populate MarketVibe database with Gift Box Campaigns and Product Promotions
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
from seller.models import Seller, Product, GiftBoxCampaign, SellerGiftBoxParticipation, Promotion

def create_gift_box_campaigns():
    """Create 10 unique gift box campaigns"""
    print("Creating Gift Box Campaigns...")
    
    # Campaign templates
    campaigns_data = [
        {
            "name": "Summer Essentials",
            "price": 149.99,
            "description": "Perfect collection for summer activities"
        },
        {
            "name": "Festive Delights",
            "price": 199.99,
            "description": "Celebrate special occasions with curated gifts"
        },
        {
            "name": "Tech Lover's Bundle",
            "price": 299.99,
            "description": "Essential gadgets for tech enthusiasts"
        },
        {
            "name": "Fitness Fanatic Pack",
            "price": 179.99,
            "description": "Everything you need for your fitness journey"
        },
        {
            "name": "Home Comfort Collection",
            "price": 129.99,
            "description": "Make your home cozy and comfortable"
        },
        {
            "name": "Outdoor Adventure Kit",
            "price": 249.99,
            "description": "Gear up for outdoor adventures"
        },
        {
            "name": "Beauty & Wellness Set",
            "price": 159.99,
            "description": "Self-care essentials for beauty and wellness"
        },
        {
            "name": "Gaming Enthusiast Box",
            "price": 349.99,
            "description": "Ultimate gaming accessories and gear"
        },
        {
            "name": "Professional Workspace",
            "price": 229.99,
            "description": "Essential items for a productive workspace"
        },
        {
            "name": "Family Fun Package",
            "price": 189.99,
            "description": "Entertainment and activities for the whole family"
        }
    ]
    
    campaigns = []
    start_date = timezone.now().date()
    
    for i, campaign_data in enumerate(campaigns_data):
        # Create campaign with dates spanning 3-6 months
        end_date = start_date + timedelta(days=random.randint(90, 180))
        
        campaign = GiftBoxCampaign.objects.create(
            name=campaign_data["name"],
            price=Decimal(str(campaign_data["price"])),
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        
        campaigns.append(campaign)
        print(f"✓ Created: {campaign.name} - ${campaign.price}")
    
    return campaigns

def assign_sellers_to_campaigns(campaigns):
    """Assign all 20 sellers to campaigns ensuring each seller is in at least one campaign"""
    print("\nAssigning sellers to campaigns...")
    
    sellers = list(Seller.objects.all())
    if not sellers:
        print("❌ No sellers found. Please run seller population script first.")
        return
    
    # Ensure each seller is assigned to at least one campaign
    for seller in sellers:
        # Assign seller to a random campaign
        campaign = random.choice(campaigns)
        
        participation, created = SellerGiftBoxParticipation.objects.get_or_create(
            seller=seller,
            campaign=campaign
        )
        
        if created:
            print(f"✓ {seller.shop_name} joined {campaign.name}")
    
    # Add some sellers to multiple campaigns for variety
    for _ in range(15):  # Add 15 more participations
        seller = random.choice(sellers)
        campaign = random.choice(campaigns)
        
        participation, created = SellerGiftBoxParticipation.objects.get_or_create(
            seller=seller,
            campaign=campaign
        )
        
        if created:
            print(f"✓ {seller.shop_name} joined {campaign.name}")
    
    # Print summary
    total_participations = SellerGiftBoxParticipation.objects.count()
    print(f"\n📊 Total campaign participations: {total_participations}")
    
    for campaign in campaigns:
        participant_count = campaign.participants.count()
        print(f"   • {campaign.name}: {participant_count} sellers")

def create_product_promotions():
    """Create 5 distinct product promotions"""
    print("\nCreating Product Promotions...")
    
    # Get all sellers with products
    sellers_with_products = Seller.objects.filter(products__isnull=False).distinct()
    
    if not sellers_with_products:
        print("❌ No sellers with products found. Please run seller and product population script first.")
        return
    
    # Promotion templates
    promotion_templates = [
        {
            "name": "Flash Sale - Electronics",
            "description": "Limited time offer on premium electronics",
            "promotion_type": "percentage",
            "discount_value": 25.0,
            "min_order_amount": 100.0,
            "max_discount_amount": 200.0
        },
        {
            "name": "Buy One Get One - Clothing",
            "description": "Buy one item, get another at 50% off",
            "promotion_type": "buy_one_get_one",
            "discount_value": 50.0,
            "min_order_amount": 50.0
        },
        {
            "name": "Free Shipping Weekend",
            "description": "Free shipping on all orders this weekend",
            "promotion_type": "free_shipping",
            "discount_value": 0.0,
            "min_order_amount": 75.0
        },
        {
            "name": "Student Discount",
            "description": "Special discount for students",
            "promotion_type": "percentage",
            "discount_value": 15.0,
            "min_order_amount": 25.0,
            "max_discount_amount": 100.0
        },
        {
            "name": "Clearance Sale",
            "description": "Deep discounts on selected items",
            "promotion_type": "percentage",
            "discount_value": 40.0,
            "min_order_amount": 30.0,
            "max_discount_amount": 150.0
        }
    ]
    
    promotions = []
    valid_from = timezone.now()
    
    for i, template in enumerate(promotion_templates):
        # Select a random seller
        seller = random.choice(sellers_with_products)
        
        # Get seller's products
        seller_products = seller.products.all()
        
        if len(seller_products) < 2:
            print(f"⚠️ Seller {seller.shop_name} has less than 2 products, skipping...")
            continue
        
        # Select 2 random products from this seller
        selected_products = random.sample(list(seller_products), 2)
        
        # Create promotion
        valid_until = valid_from + timedelta(days=random.randint(30, 90))
        
        promotion = Promotion.objects.create(
            seller=seller,
            name=template["name"],
            description=template["description"],
            promotion_type=template["promotion_type"],
            discount_value=template["discount_value"],
            min_order_amount=template["min_order_amount"],
            max_discount_amount=template.get("max_discount_amount"),
            valid_from=valid_from,
            valid_until=valid_until,
            is_active=True,
            usage_limit=random.randint(50, 200)
        )
        
        # Add products to promotion
        promotion.products.set(selected_products)
        
        promotions.append(promotion)
        
        print(f"✓ Created: {promotion.name} by {seller.shop_name}")
        print(f"  Products: {', '.join([p.name for p in selected_products])}")
        print(f"  Discount: {template['discount_value']}% (min order: ${template['min_order_amount']})")
    
    return promotions

def validate_data_integrity():
    """Validate that all data is properly created and relationships are maintained"""
    print("\n🔍 Validating Data Integrity...")
    
    # Check gift box campaigns
    campaign_count = GiftBoxCampaign.objects.count()
    print(f"✓ Gift Box Campaigns: {campaign_count}")
    
    # Check seller participations
    participation_count = SellerGiftBoxParticipation.objects.count()
    print(f"✓ Seller Participations: {participation_count}")
    
    # Check that all sellers are in at least one campaign
    sellers_in_campaigns = Seller.objects.filter(giftbox_participations__isnull=False).distinct().count()
    total_sellers = Seller.objects.count()
    print(f"✓ Sellers in campaigns: {sellers_in_campaigns}/{total_sellers}")
    
    # Check promotions
    promotion_count = Promotion.objects.count()
    print(f"✓ Product Promotions: {promotion_count}")
    
    # Check promotion products
    promotions_with_products = Promotion.objects.filter(products__isnull=False).distinct().count()
    print(f"✓ Promotions with products: {promotions_with_products}")
    
    # Validate specific relationships
    print("\n📋 Detailed Validation:")
    
    # Check each campaign
    for campaign in GiftBoxCampaign.objects.all():
        participant_count = campaign.participants.count()
        print(f"   • {campaign.name}: {participant_count} sellers, ${campaign.price}")
    
    # Check each promotion
    for promotion in Promotion.objects.all():
        product_count = promotion.products.count()
        print(f"   • {promotion.name} ({promotion.seller.shop_name}): {product_count} products, {promotion.discount_value}% off")
    
    # Check seller participation distribution
    print("\n📊 Seller Participation Distribution:")
    for seller in Seller.objects.all():
        campaign_count = seller.giftbox_participations.count()
        promotion_count = seller.promotions.count()
        print(f"   • {seller.shop_name}: {campaign_count} campaigns, {promotion_count} promotions")

def main():
    """Main function to populate gift box campaigns and promotions"""
    print("Starting to populate Gift Box Campaigns and Product Promotions...")
    print("=" * 70)
    
    # Check prerequisites
    if not Seller.objects.exists():
        print("❌ No sellers found. Please run seller population script first.")
        return
    
    if not Product.objects.exists():
        print("❌ No products found. Please run product population script first.")
        return
    
    # Create gift box campaigns
    campaigns = create_gift_box_campaigns()
    
    # Assign sellers to campaigns
    assign_sellers_to_campaigns(campaigns)
    
    # Create product promotions
    promotions = create_product_promotions()
    
    # Validate data integrity
    validate_data_integrity()
    
    print("\n" + "=" * 70)
    print("✅ Gift Box Campaigns and Promotions populated successfully!")
    print("=" * 70)
    
    # Print final summary
    print("\n📈 Final Summary:")
    print(f"   • Gift Box Campaigns: {GiftBoxCampaign.objects.count()}")
    print(f"   • Seller Participations: {SellerGiftBoxParticipation.objects.count()}")
    print(f"   • Product Promotions: {Promotion.objects.count()}")
    print(f"   • Total Sellers: {Seller.objects.count()}")
    print(f"   • Total Products: {Product.objects.count()}")
    
    # Print sample data
    print("\n🎁 Sample Gift Box Campaigns:")
    for campaign in GiftBoxCampaign.objects.all()[:5]:
        participants = campaign.participants.count()
        print(f"   • {campaign.name} - ${campaign.price} ({participants} sellers)")
    
    print("\n📢 Sample Product Promotions:")
    for promotion in Promotion.objects.all()[:5]:
        products = promotion.products.count()
        print(f"   • {promotion.name} - {promotion.discount_value}% off ({products} products)")

if __name__ == "__main__":
    main() 