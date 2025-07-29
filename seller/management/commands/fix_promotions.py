from django.core.management.base import BaseCommand
from seller.models import Promotion
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Fix promotion dates that are causing countdown issues'

    def handle(self, *args, **options):
        self.stdout.write("=== Checking and fixing promotions ===")
        
        # Get all promotions
        promotions = Promotion.objects.all()
        
        for promo in promotions:
            self.stdout.write(f"\nPromotion: {promo.name}")
            self.stdout.write(f"  Current valid_from: {promo.valid_from}")
            self.stdout.write(f"  Current valid_until: {promo.valid_until}")
            self.stdout.write(f"  Is active: {promo.is_active}")
            
            # Check if valid_until is in the past
            now = timezone.now()
            if promo.valid_until < now:
                self.stdout.write(f"  ❌ EXPIRED: valid_until ({promo.valid_until}) is in the past")
                
                # Fix: Set valid_until to 30 days from now
                new_valid_until = now + timedelta(days=30)
                promo.valid_until = new_valid_until
                promo.save()
                self.stdout.write(f"  ✅ FIXED: Set valid_until to {new_valid_until}")
            else:
                self.stdout.write(f"  ✅ VALID: valid_until ({promo.valid_until}) is in the future")
            
            # Check if valid_from is in the future
            if promo.valid_from > now:
                self.stdout.write(f"  ❌ FUTURE: valid_from ({promo.valid_from}) is in the future")
                
                # Fix: Set valid_from to now
                promo.valid_from = now
                promo.save()
                self.stdout.write(f"  ✅ FIXED: Set valid_from to {now}")
            else:
                self.stdout.write(f"  ✅ VALID: valid_from ({promo.valid_from}) is in the past")
        
        self.stdout.write("\n=== Promotion check complete ===") 