from django.urls import path
from . import views

app_name = 'buyer'

urlpatterns = [
    path('buyer/profile/', views.buyer_profile_view, name='buyer_profile'),
    path('buyer/profile/update/', views.update_buyer_view, name='buyer_update'),
    path('buyer/profile/delete/', views.delete_buyer_view, name='buyer_delete'),
]

urlpatterns += [
    path('cart/', views.get_cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/page/', views.cart_page_view, name='cart_page'),
]