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
    
    path('products/create/', views.create_product_view, name='product_create'),
    path('products/<int:product_id>/', views.product_page_view, name='product_page'),
    path('products/<int:product_id>/update/', views.update_product_view, name='product_update'),
    path('products/<int:product_id>/update/form/', views.update_product_form_view, name='product_update_form'),
    path('products/<int:product_id>/delete/', views.delete_product_view, name='product_delete'),
    
    # AJAX URLs for dynamic form
    path('ajax/get-category-children/', views.get_category_children, name='get_category_children'),
    path('ajax/get-category-attributes/', views.get_category_attributes, name='get_category_attributes'),
    path('ajax/save-attribute-value/', views.save_attribute_value, name='save_attribute_value'),

    path('dashboard/', views.seller_dashboard_overview, name='seller_dashboard'),
    path('orders/', views.seller_orders, name='seller_orders'),
    path('revenue/', views.seller_revenue, name='seller_revenue'),
    path('stripe/status/', views.seller_stripe_status, name='seller_stripe_status'),
    
    path('orders/list/', views.seller_orders_list, name='orders_list'),
    path('products/list/', views.seller_products_list, name='products_list'),
    path('products/add/', views.create_product_view, name='product_create'),
    path('products/<int:product_id>/edit/', views.seller_edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.seller_delete_product, name='delete_product'),
    path('reports/', views.seller_reports, name='reports'),
    path('profile/edit/', views.seller_edit_profile, name='edit_profile'),
    path('promotions/create/', views.seller_create_promotion, name='create_promotion'),
    path('export/', views.seller_export_data, name='export_data'),

    # Enhanced Dashboard URLs
    path('product/<int:product_id>/edit/', views.product_edit_data, name='product_edit_data'),
    path('product/<int:product_id>/update/', views.product_update, name='product_update'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:product_id>/duplicate/', views.product_duplicate, name='product_duplicate'),
    path('order/<int:order_id>/details/', views.order_details, name='order_details'),
    path('order/update-status/', views.order_update_status, name='order_update_status'),
    path('promotion/create/', views.promotion_create, name='promotion_create'),
    path('export-data/', views.export_data, name='export_data'),
    path('check-new-orders/', views.check_new_orders, name='check_new_orders'),
    path('check-low-stock/', views.check_low_stock, name='check_low_stock'),
    
    # Notification Management URLs
    path('notification/mark-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('notification/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('activity/mark-cleared/', views.mark_activity_as_cleared, name='mark_activity_as_cleared'),
    path('activity/clear-all/', views.clear_all_activity, name='clear_all_activity'),
]
