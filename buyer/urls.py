from django.urls import path
from . import views
from .views import order_summary_view

app_name = 'buyer'

urlpatterns = [
    path('buyer/profile/', views.buyer_profile_view, name='buyer_profile'),
    path('buyer/profile/update/', views.update_buyer_view, name='buyer_update'),
    path('buyer/profile/delete/', views.delete_buyer_view, name='buyer_delete'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout/', views.checkout_view, name='checkout_page'),
]

urlpatterns += [
    path('cart/', views.get_cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/page/', views.cart_page_view, name='cart_page'),
    path('cart/remove-all/', views.remove_all_from_cart, name='remove_all_from_cart'),
    path('stripe/process-payment/', views.process_stripe_payment, name='process_stripe_payment'),
    path('place-order/', views.place_order_view, name='place_order'),
]