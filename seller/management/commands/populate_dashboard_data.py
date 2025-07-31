from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from seller.models import Seller, Promotion, GiftBoxCampaign, SellerGiftBoxParticipation
from buyer.models import Buyer, GiftBoxOrder
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate sample data for dashboard tabs (promotions and gift boxes)'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for dashboard...')
        
        # Get the first seller (or create one if none exists)
        try:
            seller = Seller.objects.first()
            if not seller:
                self.stdout.write('No seller found. Please create a seller first.')
                return
        except Seller.DoesNotExist:
            self.stdout.write('No seller found. Please create a seller first.')
            return
        
        # Get the first buyer (or create one if none exists)
        try:
            buyer = Buyer.objects.first()
            if not buyer:
                self.stdout.write('No buyer found. Please create a buyer first.')
                return
        except Buyer.DoesNotExist:
            self.stdout.write('No buyer found. Please create a buyer first.')
            return

        # Create sample promotions
        self.stdout.write('Creating sample promotions...')
        
        # Promotion 1: Percentage discount
        promotion1, created = Promotion.objects.get_or_create(
            seller=seller,
            name="Summer Sale 20% Off",
            defaults={
                'description': 'Get 20% off on all summer items',
                'promotion_type': 'percentage',
                'discount_value': 20.0,
                'min_order_amount': 50.0,
                'max_discount_amount': 100.0,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=30),
                'is_active': True,
                'usage_limit': 100,
                'used_count': 15,
            }
        )
        if created:
            self.stdout.write(f'Created promotion: {promotion1.name}')
        
        # Promotion 2: Fixed amount discount
        promotion2, created = Promotion.objects.get_or_create(
            seller=seller,
            name="Free Shipping on Orders Over $100",
            defaults={
                'description': 'Free shipping for orders over $100',
                'promotion_type': 'fixed',
                'discount_value': 15.0,
                'min_order_amount': 100.0,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=60),
                'is_active': True,
                'usage_limit': 50,
                'used_count': 8,
            }
        )
        if created:
            self.stdout.write(f'Created promotion: {promotion2.name}')
        
        # Promotion 3: Buy One Get One
        promotion3, created = Promotion.objects.get_or_create(
            seller=seller,
            name="Buy One Get One Free",
            defaults={
                'description': 'Buy one item, get one free on selected products',
                'promotion_type': 'buy_one_get_one',
                'discount_value': 50.0,
                'min_order_amount': 25.0,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=15),
                'is_active': True,
                'usage_limit': 25,
                'used_count': 5,
            }
        )
        if created:
            self.stdout.write(f'Created promotion: {promotion3.name}')

        # Create sample gift box campaigns
        self.stdout.write('Creating sample gift box campaigns...')
        
        # Campaign 1: Mystery Box
        campaign1, created = GiftBoxCampaign.objects.get_or_create(
            name="Mystery Surprise Box",
            defaults={
                'price': Decimal('25.00'),
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=90)).date(),
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'Created campaign: {campaign1.name}')
        
        # Campaign 2: Premium Gift Box
        campaign2, created = GiftBoxCampaign.objects.get_or_create(
            name="Premium Gift Collection",
            defaults={
                'price': Decimal('50.00'),
                'start_date': timezone.now().date(),
                'end_date': (timezone.now() + timedelta(days=60)).date(),
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'Created campaign: {campaign2.name}')

        # Join seller to campaigns
        participation1, created = SellerGiftBoxParticipation.objects.get_or_create(
            seller=seller,
            campaign=campaign1,
        )
        if created:
            self.stdout.write(f'Seller joined campaign: {campaign1.name}')
        
        participation2, created = SellerGiftBoxParticipation.objects.get_or_create(
            seller=seller,
            campaign=campaign2,
        )
        if created:
            self.stdout.write(f'Seller joined campaign: {campaign2.name}')

        # Create sample gift box orders
        self.stdout.write('Creating sample gift box orders...')
        
        # Order 1: Pending
        order1, created = GiftBoxOrder.objects.get_or_create(
            buyer=buyer,
            seller=seller,
            campaign=campaign1,
            defaults={
                'status': 'pending',
                'buyer_message': 'Birthday gift for my sister',
                'created_at': timezone.now() - timedelta(days=2),
            }
        )
        if created:
            self.stdout.write(f'Created gift box order: #{order1.id}')
        
        # Order 2: Packed
        order2, created = GiftBoxOrder.objects.get_or_create(
            buyer=buyer,
            seller=seller,
            campaign=campaign2,
            defaults={
                'status': 'packed',
                'buyer_message': 'Anniversary surprise',
                'created_at': timezone.now() - timedelta(days=5),
            }
        )
        if created:
            self.stdout.write(f'Created gift box order: #{order2.id}')
        
        # Order 3: Shipped
        order3, created = GiftBoxOrder.objects.get_or_create(
            buyer=buyer,
            seller=seller,
            campaign=campaign1,
            defaults={
                'status': 'shipped',
                'buyer_message': 'Just because gift',
                'created_at': timezone.now() - timedelta(days=10),
            }
        )
        if created:
            self.stdout.write(f'Created gift box order: #{order3.id}')
        
        # Order 4: Delivered
        order4, created = GiftBoxOrder.objects.get_or_create(
            buyer=buyer,
            seller=seller,
            campaign=campaign2,
            defaults={
                'status': 'delivered',
                'buyer_message': 'Thank you gift',
                'created_at': timezone.now() - timedelta(days=15),
            }
        )
        if created:
            self.stdout.write(f'Created gift box order: #{order4.id}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for dashboard tabs!')
        )
        self.stdout.write('Sample data includes:')
        self.stdout.write('- 3 active promotions')
        self.stdout.write('- 2 gift box campaigns')
        self.stdout.write('- 4 gift box orders with different statuses')
        self.stdout.write('You can now view the data in the dashboard tabs.') 