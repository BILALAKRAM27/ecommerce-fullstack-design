from .models import Buyer
from seller.models import Seller

def user_sidebar_data(request):
    """Context processor to provide user data for the sidebar across all templates"""
    context = {
        'user_type': None,
        'buyer': None,
        'seller': None,
        'image_base64': None
    }
    
    # Check if request has user attribute
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            # Try to get buyer profile
            buyer = Buyer.objects.filter(email=request.user.email).first()
            if buyer:
                context.update({
                    'user_type': 'buyer',
                    'buyer': buyer,
                    'image_base64': buyer.get_image_base64() if buyer.image else None
                })
                return context
        except Buyer.DoesNotExist:
            pass

        try:
            # Try to get seller profile
            seller = Seller.objects.filter(email=request.user.email).first()
            if seller:
                context.update({
                    'user_type': 'seller',
                    'seller': seller,
                    'image_base64': seller.get_image_base64() if seller.image else None
                })
                return context
        except Seller.DoesNotExist:
            pass

    return context 