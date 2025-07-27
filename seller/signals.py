from django.db.models.signals import post_save
from django.dispatch import receiver
from buyer.models import Order, BuyerNotification, Wishlist
from .models import Activity, Notification

@receiver(post_save, sender=Order)
def create_order_activity(sender, instance, created, **kwargs):
    """Create activity when a new order is placed"""
    if created:
        # Check if activity already exists for this order
        if not Activity.objects.filter(
            seller=instance.seller,
            title=f'Order #{instance.id} Placed'
        ).exists():
            # Create activity for new order
            Activity.objects.create(
                seller=instance.seller,
                type='order_placed',
                title=f'Order #{instance.id} Placed',
                description=f'New order received from {instance.buyer.name if hasattr(instance.buyer, "name") else instance.buyer.user.username} for ${instance.total_amount}'
            )
        
        # Check if notification already exists for this order
        if not Notification.objects.filter(
            seller=instance.seller,
            title='New Order Received',
            message__contains=f'Order #{instance.id}'
        ).exists():
            # Create notification for new order
            Notification.objects.create(
                seller=instance.seller,
                type='order',
                title='New Order Received',
                message=f'Order #{instance.id} has been placed for ${instance.total_amount}'
            )

@receiver(post_save, sender='seller.Product')
def create_product_activity(sender, instance, created, **kwargs):
    """Create activity when a product is created or updated"""
    if created:
        # Create activity for new product
        Activity.objects.create(
            seller=instance.seller,
            type='product_added',
            title=f'Product Added: {instance.name}',
            description=f'New product "{instance.name}" has been added to your inventory'
        )
        
        # Check if new product has low stock (15 or less)
        if instance.stock <= 15 and instance.stock > 0:
            # Create low stock notification for seller
            Notification.objects.create(
                seller=instance.seller,
                type='stock',
                title='Low Stock Alert',
                message=f'Product "{instance.name}" was added with low stock (only {instance.stock} available)'
            )
            
            # Create low stock notifications for buyers who have this product in their wishlist
            wishlist_buyers = Wishlist.objects.filter(product=instance).select_related('buyer')
            for wishlist_item in wishlist_buyers:
                buyer = wishlist_item.buyer
                BuyerNotification.objects.create(
                    buyer=buyer,
                    type='stock',
                    title='Low Stock Alert',
                    message=f'Product "{instance.name}" from {instance.seller.shop_name} is running low on stock (only {instance.stock} left). Order soon to avoid missing out!'
                )
    else:
        # Check if stock was updated and is now low (15 or less)
        if hasattr(instance, '_state') and instance._state.fields_cache.get('stock', None) is not None:
            old_stock = instance._state.fields_cache['stock']
            if old_stock > 15 and instance.stock <= 15 and instance.stock > 0:
                # Create low stock notification for seller
                if not Notification.objects.filter(
                    seller=instance.seller,
                    type='stock',
                    message__contains=instance.name
                ).exists():
                    Notification.objects.create(
                        seller=instance.seller,
                        type='stock',
                        title='Low Stock Alert',
                        message=f'Product "{instance.name}" is running low on stock (only {instance.stock} left)'
                    )
                
                # Create low stock notifications for buyers who have this product in their wishlist
                wishlist_buyers = Wishlist.objects.filter(product=instance).select_related('buyer')
                for wishlist_item in wishlist_buyers:
                    buyer = wishlist_item.buyer
                    # Check if notification already exists for this buyer and product
                    if not BuyerNotification.objects.filter(
                        buyer=buyer,
                        type='stock',
                        message__contains=instance.name
                    ).exists():
                        BuyerNotification.objects.create(
                            buyer=buyer,
                            type='stock',
                            title='Low Stock Alert',
                            message=f'Product "{instance.name}" from {instance.seller.shop_name} is running low on stock (only {instance.stock} left). Order soon to avoid missing out!'
                        )

@receiver(post_save, sender='buyer.Wishlist')
def check_wishlist_low_stock(sender, instance, created, **kwargs):
    """Check if a product added to wishlist has low stock"""
    if created:
        product = instance.product
        # Check if the product has low stock (15 or less)
        if product.stock <= 15 and product.stock > 0:
            # Create notification for buyer
            if not BuyerNotification.objects.filter(
                buyer=instance.buyer,
                type='stock',
                message__contains=product.name
            ).exists():
                BuyerNotification.objects.create(
                    buyer=instance.buyer,
                    type='stock',
                    title='Low Stock Alert',
                    message=f'Product "{product.name}" from {product.seller.shop_name} is running low on stock (only {product.stock} left). Order soon to avoid missing out!'
                ) 