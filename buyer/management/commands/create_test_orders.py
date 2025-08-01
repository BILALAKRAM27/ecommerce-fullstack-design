from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from buyer.models import Buyer, Order, GiftBoxOrder
from seller.models import Seller, GiftBoxCampaign, Promotion
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create test orders for buyers'

    def handle(self, *args, **options):
        # Create a test seller if it doesn't exist
        seller, created = Seller.objects.get_or_create(
            email='test@seller.com',
            defaults={
                'name': 'Test Seller',
                'shop_name': 'Test Shop',
                'shop_description': 'A test shop for testing orders'
            }
        )
        
        if created:
            self.stdout.write(f'Created test seller: {seller.shop_name}')
        
        # Create a test buyer if it doesn't exist
        buyer, created = Buyer.objects.get_or_create(
            email='buyer2@example.com',
            defaults={
                'name': 'Test Buyer',
                'phone': '+1234567890'
            }
        )
        
        if created:
            self.stdout.write(f'Created test buyer: {buyer.name}')
        
        # Create a test gift box campaign if it doesn't exist
        campaign, created = GiftBoxCampaign.objects.get_or_create(
            name='Test Gift Box',
            defaults={
                'price': 50.00,
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timedelta(days=30),
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created test campaign: {campaign.name}')
        
        # Create a test promotion
        promotion, created = Promotion.objects.get_or_create(
            name='Summer Sale 20% Off',
            seller=seller,
            defaults={
                'description': 'Get 20% off on all summer products',
                'promotion_type': 'percentage',
                'discount_value': 20.0,
                'min_order_amount': 50.0,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=30),
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created test promotion: {promotion.name}')
        
        # Create some test regular orders
        orders_created = 0
        for i in range(3):
            order, created = Order.objects.get_or_create(
                buyer=buyer,
                seller=seller,
                total_amount=100.00 + (i * 25),
                defaults={
                    'status': 'pending' if i == 0 else 'processing' if i == 1 else 'shipped',
                    'payment_status': 'paid',
                    'order_type': 'cod' if i % 2 == 0 else 'stripe',
                    'promotion': promotion if i == 1 else None,  # Apply promotion to second order
                    'delivery_address': f'Test Address {i+1}, Test City, Test Country',
                    'tracking_number': f'TRK{i+1:06d}' if i > 0 else None,
                    'expected_delivery_date': timezone.now().date() + timedelta(days=7 + i),
                    'created_at': timezone.now() - timedelta(days=i)
                }
            )
            
            if created:
                orders_created += 1
                self.stdout.write(f'Created regular order: {order.order_number}')
        
        # Create some test gift box orders
        giftbox_orders_created = 0
        for i in range(2):
            order, created = GiftBoxOrder.objects.get_or_create(
                buyer=buyer,
                seller=seller,
                campaign=campaign,
                defaults={
                    'status': 'pending' if i == 0 else 'packed',
                    'payment_status': 'paid' if i == 1 else 'pending',
                    'order_type': 'stripe' if i == 1 else 'cod',
                    'promotion': promotion if i == 0 else None,  # Apply promotion to first gift box order
                    'buyer_message': f'Test message for gift box {i+1}',
                    'delivery_address': f'Gift Box Address {i+1}, Test City, Test Country',
                    'tracking_number': f'GB{i+1:06d}' if i > 0 else None,
                    'expected_delivery_date': timezone.now().date() + timedelta(days=5 + i),
                    'total_amount': 50.00 + (i * 10),
                    'created_at': timezone.now() - timedelta(days=i+1)
                }
            )
            
            if created:
                giftbox_orders_created += 1
                self.stdout.write(f'Created gift box order: {order.order_number}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {orders_created} regular orders and {giftbox_orders_created} gift box orders'
            )
        ) 