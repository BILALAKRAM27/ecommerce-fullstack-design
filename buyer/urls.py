from django.urls import path
from . import views

app_name = 'buyer'

urlpatterns = [
    path('buyer/profile/', views.buyer_profile_view, name='buyer_profile'),
    path('buyer/profile/update/', views.update_buyer_view, name='buyer_update'),
    path('buyer/profile/delete/', views.delete_buyer_view, name='buyer_delete'),
]