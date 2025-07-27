from django.core.management.base import BaseCommand
from seller.models import Seller, Activity, Notification
from buyer.models import Order
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate activities and notifications for existing orders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seller-id',
            type=int,
            help='Specific seller ID to populate data for',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of activities and notifications',
        )

    def handle(self, *args, **options):
        seller_id = options.get('seller_id')
        force = options.get('force')
        
        if seller_id:
            sellers = Seller.objects.filter(id=seller_id)
        else:
            sellers = Seller.objects.all()
        
        for seller in sellers:
            self.stdout.write(f"Processing seller: {seller.shop_name}")
            
            # Get recent orders for this seller
            recent_orders = Order.objects.filter(seller=seller).order_by('-created_at')[:10]
            
            if not recent_orders.exists():
                self.stdout.write(f"No orders found for seller {seller.shop_name}")
                continue
            
            # Check if activities already exist
            existing_activities = Activity.objects.filter(seller=seller)
            if existing_activities.exists() and not force:
                self.stdout.write(f"Activities already exist for seller {seller.shop_name}, skipping...")
                continue
            
            # Create activities for recent orders
            activities_created = 0
            for order in recent_orders:
                # Check if activity already exists for this order
                if not force and Activity.objects.filter(
                    seller=seller, 
                    title=f'Order #{order.id} Placed'
                ).exists():
                    continue
                
                Activity.objects.create(
                    seller=seller,
                    type='order_placed',
                    title=f'Order #{order.id} Placed',
                    description=f'New order received from {order.buyer.name if hasattr(order.buyer, "name") else order.buyer.user.username} for ${order.total_amount}'
                )
                activities_created += 1
            
            # Check if notifications already exist
            existing_notifications = Notification.objects.filter(seller=seller)
            if existing_notifications.exists() and not force:
                self.stdout.write(f"Notifications already exist for seller {seller.shop_name}, skipping...")
                continue
            
            # Create notifications
            notifications_created = 0
            
            # Count pending orders
            pending_orders = Order.objects.filter(seller=seller, status='pending').count()
            if pending_orders > 0:
                Notification.objects.create(
                    seller=seller,
                    type='order',
                    title='New Order Received',
                    message=f'You have {pending_orders} pending orders'
                )
                notifications_created += 1
            
            # Count low stock products (15 or less)
            low_stock_products = seller.products.filter(stock__lte=15, stock__gt=0).count()
            if low_stock_products > 0:
                Notification.objects.create(
                    seller=seller,
                    type='stock',
                    title='Low Stock Alert',
                    message=f'{low_stock_products} products are running low on stock (15 or less items)'
                )
                notifications_created += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {activities_created} activities and {notifications_created} notifications for seller {seller.shop_name}"
                )
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated activities and notifications')) 