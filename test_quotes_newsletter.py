#!/usr/bin/env python
"""
Test script for Quotes System and Newsletter Subscription features
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import QuoteRequest, QuoteResponse, NewsletterSubscriber, Category, Seller
from buyer.models import Buyer
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def test_quotes_system():
    """Test the quotes system functionality"""
    print("Testing Quotes System...")
    
    # Check if we have categories
    categories = Category.objects.all()
    if not categories.exists():
        print("❌ No categories found. Please populate categories first.")
        return False
    
    # Check if we have buyers
    buyers = Buyer.objects.all()
    if not buyers.exists():
        print("❌ No buyers found. Please create buyer accounts first.")
        return False
    
    # Check if we have sellers
    sellers = Seller.objects.all()
    if not sellers.exists():
        print("❌ No sellers found. Please create seller accounts first.")
        return False
    
    print("✅ Basic data available for quotes system")
    
    # Test creating a quote request
    try:
        buyer = buyers.first()
        category = categories.first()
        
        quote_request = QuoteRequest.objects.create(
            buyer=buyer,
            category=category,
            product_name="Test Product",
            description="This is a test quote request",
            quantity=10,
            unit='pcs',
            urgency='medium',
            budget_range='$100-500',
            expires_at=timezone.now() + timedelta(days=30)
        )
        print(f"✅ Created quote request: {quote_request}")
        
        # Test creating a quote response
        seller = sellers.first()
        quote_response = QuoteResponse.objects.create(
            quote_request=quote_request,
            seller=seller,
            price=25.50,
            delivery_estimate="3-5 business days",
            notes="We can provide this product at competitive pricing"
        )
        print(f"✅ Created quote response: {quote_response}")
        
        # Test quote request methods
        print(f"✅ Quote request responses count: {quote_request.get_responses_count()}")
        print(f"✅ Quote request is expired: {quote_request.is_expired}")
        
        # Clean up test data
        quote_response.delete()
        quote_request.delete()
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing quotes system: {e}")
        return False

def test_newsletter_subscription():
    """Test the newsletter subscription functionality"""
    print("\nTesting Newsletter Subscription...")
    
    try:
        # Test creating a newsletter subscriber
        subscriber = NewsletterSubscriber.objects.create(
            email="test@example.com",
            role='buyer',
            receive_product_updates=True,
            receive_platform_announcements=True,
            receive_seller_tools=False,
            receive_buyer_recommendations=True
        )
        print(f"✅ Created newsletter subscriber: {subscriber}")
        print(f"✅ Preferences summary: {subscriber.preferences_summary}")
        
        # Test duplicate prevention
        try:
            duplicate_subscriber = NewsletterSubscriber.objects.create(
                email="test@example.com",
                role='seller'
            )
            print("❌ Duplicate subscription should not be allowed")
            return False
        except:
            print("✅ Duplicate subscription correctly prevented")
        
        # Clean up test data
        subscriber.delete()
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing newsletter subscription: {e}")
        return False

def test_urls():
    """Test that all URLs are properly configured"""
    print("\nTesting URL Configuration...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test quote URLs
        urls_to_test = [
            'sellers:submit_quote_request',
            'sellers:seller_quotes_inbox',
            'sellers:buyer_quote_requests',
            'sellers:subscribe_newsletter',
            'sellers:manage_newsletter_subscription',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ URL {url_name}: {url}")
            except Exception as e:
                print(f"❌ URL {url_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing URLs: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing Quotes System and Newsletter Subscription")
    print("=" * 50)
    
    tests = [
        test_quotes_system,
        test_newsletter_subscription,
        test_urls,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The quotes system and newsletter subscription are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 