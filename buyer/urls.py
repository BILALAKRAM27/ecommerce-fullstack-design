from django.urls import path
from . import views
from .views import order_summary_view, giftbox_marketplace_view, buy_giftbox_view, giftbox_orders_view

app_name = 'buyer'

urlpatterns = [
    path('buyer/profile/', views.buyer_profile_view, name='buyer_profile'),
    path('buyer/profile/update/', views.update_buyer_view, name='buyer_update'),
    path('buyer/profile/delete/', views.delete_buyer_view, name='buyer_delete'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/check/', views.check_wishlist_status, name='check_wishlist_status'),
    path('checkout/', views.checkout_view, name='checkout_page'),
    path('promotion/checkout/', views.promotion_checkout_view, name='promotion_checkout'),
]

urlpatterns += [
    path('cart/', views.get_cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/check/', views.check_cart_status, name='check_cart_status'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/page/', views.cart_page_view, name='cart_page'),
    path('cart/remove-all/', views.remove_all_from_cart, name='remove_all_from_cart'),
    path('stripe/process-payment/', views.process_stripe_payment, name='process_stripe_payment'),
    path('place-order/', views.place_order_view, name='place_order'),
    path('fetch-order-details/', views.fetch_order_details, name='fetch_order_details'),
    
    # Buyer Notification Management URLs
    path('notification/mark-read/', views.mark_buyer_notification_as_read, name='mark_buyer_notification_as_read'),
    path('notification/mark-all-read/', views.mark_all_buyer_notifications_as_read, name='mark_all_buyer_notifications_as_read'),
    path('notification/clear-all/', views.clear_all_buyer_notifications, name='clear_all_buyer_notifications'),
]

urlpatterns += [
    path('gift-boxes/', giftbox_marketplace_view, name='giftbox_marketplace'),
    path('gift-boxes/buy/<int:seller_id>/', buy_giftbox_view, name='buy_giftbox'),
    path('gift-boxes/orders/', giftbox_orders_view, name='giftbox_orders'),
]