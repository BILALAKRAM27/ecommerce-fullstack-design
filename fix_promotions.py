#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Promotion
from django.utils import timezone

def fix_promotions():
    """Fix existing promotions with incorrect dates"""
    print("=== Checking and fixing promotions ===")
    
    # Get all promotions
    promotions = Promotion.objects.all()
    
    for promo in promotions:
        print(f"\nPromotion: {promo.name}")
        print(f"  Current valid_from: {promo.valid_from}")
        print(f"  Current valid_until: {promo.valid_until}")
        print(f"  Is active: {promo.is_active}")
        
        # Check if valid_until is in the past
        now = timezone.now()
        if promo.valid_until < now:
            print(f"  ❌ EXPIRED: valid_until ({promo.valid_until}) is in the past")
            
            # Fix: Set valid_until to 30 days from now
            new_valid_until = now + timedelta(days=30)
            promo.valid_until = new_valid_until
            promo.save()
            print(f"  ✅ FIXED: Set valid_until to {new_valid_until}")
        else:
            print(f"  ✅ VALID: valid_until ({promo.valid_until}) is in the future")
        
        # Check if valid_from is in the future
        if promo.valid_from > now:
            print(f"  ❌ FUTURE: valid_from ({promo.valid_from}) is in the future")
            
            # Fix: Set valid_from to now
            promo.valid_from = now
            promo.save()
            print(f"  ✅ FIXED: Set valid_from to {now}")
        else:
            print(f"  ✅ VALID: valid_from ({promo.valid_from}) is in the past")
    
    print("\n=== Promotion check complete ===")

if __name__ == "__main__":
    fix_promotions() 