from django.urls import path
from . import views
from .views import giftbox_campaigns_view, join_giftbox_campaign, giftbox_orders_seller_view, fulfill_giftbox_order_view

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
    path('ajax/get-filtered-products/', views.get_filtered_products, name='get_filtered_products'),

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
    path('product/<int:product_id>/update/', views.product_update, name='product_update_simple'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:product_id>/duplicate/', views.product_duplicate, name='product_duplicate'),
    path('order/<int:order_id>/details/', views.order_details, name='order_details'),
    path('order/update-status/', views.order_update_status, name='order_update_status'),
    
    # Hot Offers URLs
    path('hot-offers/', views.hot_offers_view, name='hot_offers'),
    path('promotion/<int:promotion_id>/', views.promotion_detail_view, name='promotion_detail'),
    path('search-promotions/', views.search_promotions_ajax, name='search_promotions'),
    path('promotion/create/', views.promotion_create, name='promotion_create'),
    path('export-data/', views.export_data, name='export_data_ajax'),
    path('check-new-orders/', views.check_new_orders, name='check_new_orders'),
    path('check-low-stock/', views.check_low_stock, name='check_low_stock'),
    path('test-export/', views.test_export, name='test_export'),
    path('simple-export-test/', views.simple_export_test, name='simple_export_test'),
    path('test-create-promotion/', views.test_create_promotion, name='test_create_promotion'),
    
    # Notification Management URLs
    path('notification/mark-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('notification/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('activity/mark-cleared/', views.mark_activity_as_cleared, name='mark_activity_as_cleared'),
    path('activity/clear-all/', views.clear_all_activity, name='clear_all_activity'),
]

urlpatterns += [
    path('giftbox-campaigns/', giftbox_campaigns_view, name='giftbox_campaigns'),
    path('giftbox-campaigns/join/<int:campaign_id>/', join_giftbox_campaign, name='join_giftbox_campaign'),
    path('giftbox-orders/', giftbox_orders_seller_view, name='giftbox_orders'),
    path('giftbox-orders/fulfill/<int:order_id>/', fulfill_giftbox_order_view, name='fulfill_giftbox_order'),
    path('buyer-info/<int:buyer_id>/', views.get_buyer_info, name='get_buyer_info'),
    path('promotions/', views.promotions_list_view, name='promotions_list'),
    path('promotions/<int:promotion_id>/delete/', views.delete_promotion, name='delete_promotion'),
    path('promotions/<int:promotion_id>/update/form/', views.promotion_update_form_view, name='promotion_update_form'),
    path('promotions/<int:promotion_id>/update/', views.promotion_update_view, name='promotion_update'),
    path('marketplace/', views.product_listing_view, name='product_listing'),
    
    # Review System URLs
    path('products/<int:product_id>/review/', views.submit_product_review, name='submit_product_review'),
    path('seller/<int:seller_id>/review/', views.submit_seller_review, name='submit_seller_review'),
    path('reviews/<str:review_type>/<int:review_id>/like/', views.like_review, name='like_review'),
    path('products/<int:product_id>/reviews/', views.get_product_reviews, name='get_product_reviews'),
    path('seller/<int:seller_id>/reviews/', views.get_seller_reviews, name='get_seller_reviews'),
    
    # New Template URLs
    path('about/', views.about_view, name='about'),
    path('find-store/', views.find_store_view, name='find_store'),
    path('partnership/', views.partnership_view, name='partnership'),
    path('information/', views.information_view, name='information'),
    path('money-refund/', views.money_refund_view, name='money_refund'),
    path('shipping/', views.shipping_view, name='shipping'),
    
    # Search functionality
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search-stores/', views.search_stores_ajax, name='search_stores_ajax'),
    path('test-sellers/', views.test_sellers_endpoint, name='test_sellers'),
    
    # ========== QUOTES SYSTEM URLs ==========
    path('quotes/submit/', views.submit_quote_request, name='submit_quote_request'),
    path('quotes/inbox/', views.seller_quotes_inbox, name='seller_quotes_inbox'),
    path('quotes/<int:quote_id>/respond/', views.respond_to_quote, name='respond_to_quote'),
    path('quotes/my-requests/', views.buyer_quote_requests, name='buyer_quote_requests'),
    path('quotes/<int:quote_id>/details/', views.quote_details, name='quote_details'),
    path('quotes/response/<int:response_id>/accept/', views.accept_quote_response, name='accept_quote_response'),
    path('quotes/response/<int:response_id>/reject/', views.reject_quote_response, name='reject_quote_response'),
    path('api/quote-responses/<int:quote_id>/', views.fetch_quote_responses, name='fetch_quote_responses'),
    
    # ========== NEWSLETTER SUBSCRIPTION URLs ==========
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('newsletter/manage/', views.manage_newsletter_subscription, name='manage_newsletter_subscription'),
    path('newsletter/unsubscribe/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
]
