#!/usr/bin/env python
"""
Script to populate MarketVibe database with Quote Requests and Responses
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
from buyer.models import Buyer
from seller.models import Seller, Category, QuoteRequest, QuoteResponse

def create_quote_requests():
    """Create quote requests from buyers"""
    print("Creating Quote Requests...")
    
    buyers = list(Buyer.objects.all())
    categories = list(Category.objects.all())
    
    if not buyers:
        print("❌ No buyers found. Please run buyer population script first.")
        return []
    
    if not categories:
        print("❌ No categories found. Please run category population script first.")
        return []
    
    # Product templates for quote requests
    product_templates = [
        {
            'name': 'Custom Electronics Assembly',
            'description': 'Need custom PCB assembly for IoT project with specific components and quality requirements.',
            'category_keywords': ['Electronics', 'Computer and Tech'],
            'quantity_range': (10, 100),
            'budget_range': '$500-$2000',
            'urgency': 'medium'
        },
        {
            'name': 'Bulk Clothing Order',
            'description': 'Looking for wholesale clothing items for retail business. Need various sizes and colors.',
            'category_keywords': ['Clothes and Wear'],
            'quantity_range': (50, 500),
            'budget_range': '$1000-$5000',
            'urgency': 'high'
        },
        {
            'name': 'Industrial Machinery Parts',
            'description': 'Require custom machined parts for industrial equipment. High precision and durability needed.',
            'category_keywords': ['Machinery Tools', 'Tools and Equipment'],
            'quantity_range': (5, 25),
            'budget_range': '$2000-$10000',
            'urgency': 'urgent'
        },
        {
            'name': 'Home Interior Furniture',
            'description': 'Custom furniture pieces for home renovation project. Modern design with quality materials.',
            'category_keywords': ['Home Interiors'],
            'quantity_range': (1, 10),
            'budget_range': '$500-$3000',
            'urgency': 'low'
        },
        {
            'name': 'Sports Equipment Bulk Order',
            'description': 'Sports equipment for school athletic program. Need various sports items in bulk.',
            'category_keywords': ['Sports and Outdoor'],
            'quantity_range': (20, 100),
            'budget_range': '$800-$4000',
            'urgency': 'medium'
        },
        {
            'name': 'Pet Supplies Wholesale',
            'description': 'Pet food and supplies for veterinary clinic. Need reliable suppliers with good pricing.',
            'category_keywords': ['Animals and Pets'],
            'quantity_range': (30, 200),
            'budget_range': '$300-$1500',
            'urgency': 'medium'
        },
        {
            'name': 'Automotive Parts Supply',
            'description': 'Automotive replacement parts for repair shop. Need quality parts with warranty.',
            'category_keywords': ['Automobiles'],
            'quantity_range': (10, 50),
            'budget_range': '$1000-$8000',
            'urgency': 'high'
        },
        {
            'name': 'Office Equipment and Supplies',
            'description': 'Complete office setup including furniture, electronics, and supplies for new business.',
            'category_keywords': ['Computer and Tech', 'Home Interiors'],
            'quantity_range': (5, 20),
            'budget_range': '$2000-$15000',
            'urgency': 'medium'
        }
    ]
    
    quote_requests = []
    
    # Create 30 quote requests
    for i in range(30):
        buyer = random.choice(buyers)
        template = random.choice(product_templates)
        
        # Find appropriate category
        matching_categories = [cat for cat in categories if any(keyword in cat.name for keyword in template['category_keywords'])]
        if not matching_categories:
            category = random.choice(categories)
        else:
            category = random.choice(matching_categories)
        
        # Generate realistic data
        quantity = random.randint(*template['quantity_range'])
        unit = random.choice(['pcs', 'kg', 'tons', 'units'])
        urgency = template['urgency']
        
        # Set delivery deadline (1-60 days from now)
        delivery_deadline = timezone.now().date() + timedelta(days=random.randint(1, 60))
        
        # Set expiration (7-30 days from creation)
        expires_at = timezone.now() + timedelta(days=random.randint(7, 30))
        
        # Create quote request
        quote_request = QuoteRequest.objects.create(
            buyer=buyer,
            category=category,
            product_name=template['name'],
            description=template['description'],
            quantity=quantity,
            unit=unit,
            urgency=urgency,
            status=random.choice(['pending', 'responded', 'accepted', 'rejected']),
            budget_range=template['budget_range'],
            delivery_deadline=delivery_deadline,
            expires_at=expires_at
        )
        
        quote_requests.append(quote_request)
        print(f"✓ Created quote request: {template['name']} by {buyer.name} (Qty: {quantity} {unit})")
    
    return quote_requests

def create_quote_responses(quote_requests):
    """Create quote responses from sellers"""
    print("\nCreating Quote Responses...")
    
    sellers = list(Seller.objects.all())
    
    if not sellers:
        print("❌ No sellers found. Please run seller population script first.")
        return []
    
    responses = []
    
    for quote_request in quote_requests:
        # 1-3 sellers respond to each quote request
        responding_sellers = random.sample(sellers, min(3, len(sellers)))
        
        for seller in responding_sellers:
            # Generate realistic pricing
            base_price_per_unit = random.uniform(10, 500)
            
            # Adjust price based on urgency and quantity
            if quote_request.urgency == 'urgent':
                base_price_per_unit *= 1.3  # 30% premium for urgent orders
            elif quote_request.urgency == 'high':
                base_price_per_unit *= 1.15  # 15% premium for high urgency
            
            # Quantity discount
            if quote_request.quantity > 100:
                base_price_per_unit *= 0.8  # 20% discount for bulk orders
            elif quote_request.quantity > 50:
                base_price_per_unit *= 0.9  # 10% discount for medium orders
            
            # Add some variation between sellers
            price_variation = random.uniform(0.8, 1.2)
            final_price_per_unit = base_price_per_unit * price_variation
            
            # Calculate delivery estimate
            if quote_request.urgency == 'urgent':
                delivery_days = random.randint(1, 7)
            elif quote_request.urgency == 'high':
                delivery_days = random.randint(3, 14)
            else:
                delivery_days = random.randint(7, 30)
            
            delivery_estimate = f"{delivery_days} days"
            
            # Generate seller notes
            seller_notes = [
                f"We can provide {quote_request.product_name} with premium quality materials.",
                f"Bulk discount available for orders over 100 units.",
                f"Express shipping available for urgent orders.",
                f"Quality guaranteed with 1-year warranty.",
                f"Custom specifications can be accommodated.",
                f"Sample available before bulk order.",
                f"Flexible payment terms available.",
                f"Local pickup available to reduce costs."
            ]
            
            notes = random.choice(seller_notes)
            
            # Determine if this response is accepted/rejected
            is_accepted = random.choice([True, False, False])  # 33% chance of being accepted
            is_rejected = random.choice([False, False, True])  # 33% chance of being rejected
            
            # Create quote response
            response = QuoteResponse.objects.create(
                quote_request=quote_request,
                seller=seller,
                price=Decimal(str(final_price_per_unit)),
                delivery_estimate=delivery_estimate,
                notes=notes,
                is_accepted=is_accepted,
                is_rejected=is_rejected
            )
            
            responses.append(response)
            print(f"✓ Created response from {seller.shop_name}: ${final_price_per_unit:.2f} per unit ({delivery_estimate})")
    
    return responses

def update_quote_request_statuses():
    """Update quote request statuses based on responses"""
    print("\nUpdating Quote Request Statuses...")
    
    for quote_request in QuoteRequest.objects.all():
        responses = quote_request.responses.all()
        
        if responses.exists():
            # Check if any response is accepted
            accepted_response = responses.filter(is_accepted=True).first()
            if accepted_response:
                quote_request.status = 'accepted'
            else:
                # Check if all responses are rejected
                all_rejected = all(response.is_rejected for response in responses)
                if all_rejected:
                    quote_request.status = 'rejected'
                else:
                    quote_request.status = 'responded'
            
            quote_request.save()
            print(f"✓ Updated quote request #{quote_request.id} status to: {quote_request.status}")

def validate_quote_data():
    """Validate that all quote data is properly created"""
    print("\n🔍 Validating Quote Data...")
    
    # Check quote requests
    quote_requests = QuoteRequest.objects.count()
    print(f"✓ Quote Requests: {quote_requests}")
    
    # Check quote responses
    quote_responses = QuoteResponse.objects.count()
    print(f"✓ Quote Responses: {quote_responses}")
    
    # Check status distribution
    status_counts = {}
    for status in ['pending', 'responded', 'accepted', 'rejected']:
        count = QuoteRequest.objects.filter(status=status).count()
        status_counts[status] = count
        print(f"   • {status.title()}: {count}")
    
    # Check response distribution
    accepted_responses = QuoteResponse.objects.filter(is_accepted=True).count()
    rejected_responses = QuoteResponse.objects.filter(is_rejected=True).count()
    pending_responses = QuoteResponse.objects.filter(is_accepted=False, is_rejected=False).count()
    
    print(f"\n📋 Response Distribution:")
    print(f"   • Accepted Responses: {accepted_responses}")
    print(f"   • Rejected Responses: {rejected_responses}")
    print(f"   • Pending Responses: {pending_responses}")
    
    # Check average responses per request
    if quote_requests > 0:
        avg_responses = quote_responses / quote_requests
        print(f"   • Average Responses per Request: {avg_responses:.1f}")
    
    # Check category distribution
    print(f"\n📂 Category Distribution:")
    category_counts = {}
    for quote_request in QuoteRequest.objects.all():
        category_name = quote_request.category.name
        category_counts[category_name] = category_counts.get(category_name, 0) + 1
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   • {category}: {count} requests")

def main():
    """Main function to populate quotes"""
    print("Starting to populate Quote Requests and Responses...")
    print("=" * 70)
    
    # Check prerequisites
    if not Buyer.objects.exists():
        print("❌ No buyers found. Please run buyer population script first.")
        return
    
    if not Seller.objects.exists():
        print("❌ No sellers found. Please run seller population script first.")
        return
    
    if not Category.objects.exists():
        print("❌ No categories found. Please run category population script first.")
        return
    
    # Create quote requests
    quote_requests = create_quote_requests()
    
    # Create quote responses
    quote_responses = create_quote_responses(quote_requests)
    
    # Update quote request statuses
    update_quote_request_statuses()
    
    # Validate data integrity
    validate_quote_data()
    
    print("\n" + "=" * 70)
    print("✅ Quote Requests and Responses populated successfully!")
    print("=" * 70)
    
    # Print final summary
    print("\n📈 Final Summary:")
    print(f"   • Quote Requests: {QuoteRequest.objects.count()}")
    print(f"   • Quote Responses: {QuoteResponse.objects.count()}")
    
    # Print sample data
    print("\n📝 Sample Quote Requests:")
    for quote_request in QuoteRequest.objects.all()[:5]:
        responses_count = quote_request.responses.count()
        print(f"   • {quote_request.product_name} by {quote_request.buyer.name}: {responses_count} responses - {quote_request.status}")
    
    print("\n💼 Sample Quote Responses:")
    for response in QuoteResponse.objects.all()[:5]:
        status = "Accepted" if response.is_accepted else "Rejected" if response.is_rejected else "Pending"
        print(f"   • {response.seller.shop_name}: ${response.price} per unit ({response.delivery_estimate}) - {status}")

if __name__ == "__main__":
    main() 