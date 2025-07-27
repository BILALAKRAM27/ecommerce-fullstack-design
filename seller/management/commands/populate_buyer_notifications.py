from django.core.management.base import BaseCommand
from buyer.models import BuyerNotification, Wishlist
from seller.models import Product

class Command(BaseCommand):
    help = 'Populate buyer notifications for low stock products in wishlists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of buyer notifications',
        )

    def handle(self, *args, **options):
        force = options.get('force')
        
        # Get all products with low stock (15 or less)
        low_stock_products = Product.objects.filter(stock__lte=15, stock__gt=0)
        
        if not low_stock_products.exists():
            self.stdout.write("No low stock products found")
            return
        
        notifications_created = 0
        
        for product in low_stock_products:
            # Get all buyers who have this product in their wishlist
            wishlist_items = Wishlist.objects.filter(product=product).select_related('buyer')
            
            for wishlist_item in wishlist_items:
                buyer = wishlist_item.buyer
                
                # Check if notification already exists for this buyer and product
                if not force and BuyerNotification.objects.filter(
                    buyer=buyer,
                    type='stock',
                    message__contains=product.name
                ).exists():
                    continue
                
                # Create notification for buyer
                BuyerNotification.objects.create(
                    buyer=buyer,
                    type='stock',
                    title='Low Stock Alert',
                    message=f'Product "{product.name}" from {product.seller.shop_name} is running low on stock (only {product.stock} left). Order soon to avoid missing out!'
                )
                notifications_created += 1
                
                self.stdout.write(
                    f"Created notification for buyer {buyer.name} for product {product.name}"
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {notifications_created} buyer notifications for low stock products'
            )
        ) 