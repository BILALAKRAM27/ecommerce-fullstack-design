from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    # Seller URLs
    path('', views.index_view, name='seller_profile'),
    path('register/', views.create_seller_view, name='register'),
    path('profile/', views.seller_profile_view, name='seller_profile'),
    path('profile/update/', views.update_seller_view, name='seller_update'),
    path('profile/delete/', views.delete_seller_view, name='seller_delete'),

   

    #auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
