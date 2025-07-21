from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.create_seller_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.seller_profile_view, name='seller_profile'),
    path('profile/update/', views.update_seller_view, name='seller_update'),
    path('profile/delete/', views.delete_seller_view, name='seller_delete'),
    
    # Product CRUD URLs
    path('products/', views.product_list_view, name='product_list'),
    path('products/create/', views.create_product_view, name='product_create'),
    path('products/<int:product_id>/', views.product_page_view, name='product_page'),
    path('products/<int:product_id>/update/', views.update_product_view, name='product_update'),
    path('products/<int:product_id>/update/form/', views.update_product_form_view, name='product_update_form'),
    path('products/<int:product_id>/delete/', views.delete_product_view, name='product_delete'),
    
    # AJAX URLs for dynamic form
    path('ajax/get-category-children/', views.get_category_children, name='get_category_children'),
    path('ajax/get-category-attributes/', views.get_category_attributes, name='get_category_attributes'),
    path('ajax/save-attribute-value/', views.save_attribute_value, name='save_attribute_value'),
]
