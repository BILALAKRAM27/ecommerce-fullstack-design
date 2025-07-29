import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Seller, Product, ProductImage, Brand, Category, CategoryAttribute, AttributeOption, ProductAttributeValue, Notification, Activity
from .forms import UserRegisterForm, SellerUpdateForm, SellerLoginForm, ProductForm, ProductImageForm, DynamicProductForm
from django.utils import timezone
from buyer.models import Buyer, Order, OrderStatus, Payment, PaymentStatus
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import os
import stripe
from django.conf import settings
from django.shortcuts import redirect
from .models import Seller
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
import csv
from io import StringIO
from buyer.models import OrderItem
import logging
from .models import Promotion
import csv
from django.utils import timezone
from django.http import HttpResponse
from seller.models import Product
from datetime import datetime


stripe.api_key = os.getenv("STRIPE_SECRET_KEY") or settings.STRIPE_SECRET_KEY


def index_view(request):
    user = request.user if request.user.is_authenticated else None
    seller = None
    buyer = None
    image_base64 = None
    user_type = None
    if user:
        # Try to get Seller by user
        try:
            seller = Seller.objects.get(user=user)
            image_base64 = seller.get_image_base64()
            user_type = 'seller'
        except Seller.DoesNotExist:
            # Try to get Buyer by email
            try:
                buyer = Buyer.objects.get(email=user.email)
                image_base64 = buyer.get_image_base64()
                user_type = 'buyer'
            except Buyer.DoesNotExist:
                pass
    # Get categories for sections
    electronics = Category.objects.filter(name__icontains='electronic')
    electronics_subs = Category.objects.filter(parent__in=electronics)
    clothing = Category.objects.filter(name__icontains='clothing')
    clothing_subs = Category.objects.filter(parent__in=clothing)
    furniture = Category.objects.filter(name__icontains='furniture')
    furniture_subs = Category.objects.filter(parent__in=furniture)
    electronics_cats = list(electronics) + list(electronics_subs)
    clothing_cats = list(clothing) + list(clothing_subs)
    furniture_cats = list(furniture) + list(furniture_subs)
    # Fetch products for each section
    electronics_products = Product.objects.filter(category__in=electronics_cats)
    clothing_products = Product.objects.filter(category__in=clothing_cats)
    furniture_products = Product.objects.filter(category__in=furniture_cats)
    
    # Get active promotions for homepage
    active_promotions = get_active_promotions_for_homepage()
    
    # Get the soonest expiring promotion for the timer
    soonest_expiring_promotion = None
    if active_promotions:
        soonest_expiring_promotion = active_promotions.first()
    
    context = {
        'user': user,
        'seller': seller,
        'buyer': buyer,
        'image_base64': image_base64,
        'user_type': user_type,
        'electronics_categories': electronics_cats,
        'clothing_categories': clothing_cats,
        'furniture_categories': furniture_cats,
        'electronics_products': electronics_products,
        'clothing_products': clothing_products,
        'furniture_products': furniture_products,
        'active_promotions': active_promotions,
        'soonest_expiring_promotion': soonest_expiring_promotion,
    }
    return render(request, "index.html", context)

# CREATE User (Buyer or Seller)
def create_seller_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the User account
            user = form.save()
            user_type = form.cleaned_data['user_type']
            
            if user_type == 'seller':
                # Create the Seller profile
                seller = Seller.objects.create(
                    user=user,
                    name=user.username,  # Use username as name
                    email=user.email,
                    shop_name=form.cleaned_data.get('shop_name', ''),
                    shop_description='',
                    address='',  # Empty address initially
                    created_at=timezone.now()
                )
                
                messages.success(request, 'Seller account created successfully!')
            else:
                # Create the Buyer profile
                buyer = Buyer.objects.create(
                    name=user.username,  # Use username as name
                    email=user.email,
                    phone=form.cleaned_data.get('phone', ''),
                    address='',  # Empty address
                    created_at=timezone.now()
                )
                
                messages.success(request, 'Buyer account created successfully!')
            
            return redirect('sellers:login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'seller/register.html', {'form': form, 'title': 'Register'})


# LOGIN View
def login_view(request):
    if request.method == 'POST':
        form = SellerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user_type = form.cleaned_data['user_type']
            
            # Log the user in
            login(request, user)
            
            messages.success(request, f'Welcome back, {user.username}!')
            
            if user_type == 'seller':
                return redirect('sellers:seller_profile')
            else:
                # Check if buyer exists
                try:
                    buyer = Buyer.objects.get(email=user.email)
                    return redirect('buyer:buyer_profile')  # You'll need to create this view
                except Buyer.DoesNotExist:
                    messages.error(request, 'This email is not registered as a buyer.')
                    logout(request)
                    return redirect('sellers:login')
    else:
        form = SellerLoginForm()
    
    return render(request, 'seller/login.html', {'form': form, 'title': 'Login'})


# LOGOUT View
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('sellers:login')


# READ Seller Profile
@login_required
def seller_profile_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        try:
            # Update basic fields
            seller.name = request.POST.get('name', seller.name)
            seller.shop_name = request.POST.get('shop_name', seller.shop_name)
            seller.shop_description = request.POST.get('shop_description', seller.shop_description)
            seller.address = request.POST.get('address', seller.address)
            
            # Handle image upload
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                # Read the image file and store as binary data
                seller.image = image_file.read()
            
            seller.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('sellers:seller_profile')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    context = {
        'seller': seller,
        'image_base64': seller.get_image_base64()
    }
    return render(request, 'seller/seller_profile.html', context)


# READ Buyer Profile



# UPDATE Seller
@login_required
def update_seller_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    if request.method == 'POST':
        form = SellerUpdateForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            seller = form.save()  # Let the form handle image upload
            seller.updated_at = timezone.now()
            seller.save()
            messages.success(request, 'Seller profile updated successfully.')
            return redirect('sellers:seller_profile')
    else:
        form = SellerUpdateForm(instance=seller)
    return render(request, 'seller/seller_update.html', {'form': form})


# DELETE Seller
@login_required
def delete_seller_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    if request.method == 'POST':
        # Store the user reference before deleting seller
        user = seller.user
        
        # Delete the seller profile
        seller.delete()
        
        # Delete the associated user account
        if user:
            user.delete()
        
        messages.success(request, 'Your seller account has been deleted.')
        return redirect('sellers:login')
    return render(request, 'seller/seller_delete.html')


# ========== PRODUCT CRUD VIEWS ==========

# CREATE Product
@login_required
def create_product_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            # Handle new images
            thumbnail_index = int(request.POST.get('thumbnail', 0))
            image_files = request.FILES.getlist('image_file')
            for idx, image_file in enumerate(image_files):
                ProductImage.objects.create(
                    product=product,
                    image=image_file.read(),
                    is_thumbnail=(idx == thumbnail_index)
                )
            # Handle existing images (if editing)
            existing_thumbnail_id = request.POST.get('existing_thumbnail')
            if existing_thumbnail_id:
                for img in product.images.all():
                    img.is_thumbnail = (str(img.id) == existing_thumbnail_id)
                    img.save()
            messages.success(request, 'Product created successfully!')
            return redirect('seller:products_list')
    else:
        form = ProductForm()
    
    # Get parent categories (categories with no parent)
    parent_categories = Category.objects.filter(parent__isnull=True)
    
    context = {
        'form': form,
        'title': 'Add New Product',
        'seller': seller,
        'parent_categories': parent_categories
    }
    return render(request, 'seller/product_form.html', context)


# READ Product List


# READ Product Detail
def product_page_view(request, product_id):
    user = request.user if request.user.is_authenticated else None
    seller = None
    user_type = None
    in_wishlist = False
    if user:
        try:
            seller = Seller.objects.get(user=user)
            user_type = 'seller'
        except Seller.DoesNotExist:
            from buyer.models import Buyer, Wishlist
            try:
                buyer = Buyer.objects.get(email=user.email)
                user_type = 'buyer'
                # Check if product is in wishlist
                in_wishlist = Wishlist.objects.filter(buyer=buyer, product_id=product_id).exists()
            except Buyer.DoesNotExist:
                pass
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'seller': seller,
        'user_type': user_type,
        'in_wishlist': in_wishlist,
        # add 'user' if you use it in the template
    }
    return render(request, 'seller/product_page.html', context)


# UPDATE Product
@login_required
def update_product_view(request, product_id):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    if request.method == 'POST':
        form = DynamicProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            # --- Image upload logic ---
            image_files = request.FILES.getlist('image_file')
            image_mode = request.POST.get('image_mode', 'add')
            if image_files:
                if image_mode == 'replace':
                    # Delete all existing images for this product
                    product.images.all().delete()
                # Handle new images
                thumbnail_index = int(request.POST.get('thumbnail', 0))
                for idx, image_file in enumerate(image_files):
                    ProductImage.objects.create(
                        product=product,
                        image=image_file.read(),
                        is_thumbnail=(idx == thumbnail_index)
                    )
            # Handle existing images (if editing)
            existing_thumbnail_id = request.POST.get('existing_thumbnail')
            if existing_thumbnail_id:
                for img in product.images.all():
                    img.is_thumbnail = (str(img.id) == existing_thumbnail_id)
                    img.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('sellers:product_page', product_id=product.id)
    else:
        form = DynamicProductForm(instance=product)
    
    # Get parent categories (categories with no parent)
    parent_categories = Category.objects.filter(parent__isnull=True)
    
    # Get current category hierarchy for pre-selection
    current_category = product.category
    parent_category = None
    child_category = None
    
    if current_category.parent:
        parent_category = current_category.parent
        child_category = current_category
    else:
        parent_category = current_category
    
    # Get existing attribute values for pre-population
    existing_attributes = {}
    for attr_value in product.attribute_values.all():
        existing_attributes[f'attribute_{attr_value.attribute.id}'] = attr_value.value
    
    context = {
        'form': form,
        'product': product,
        'title': 'Update Product',
        'seller': seller,
        'parent_categories': parent_categories,
        'current_parent_category': parent_category,
        'current_child_category': child_category,
        'existing_attributes': existing_attributes
    }
    return render(request, 'seller/product_form.html', context)


# AJAX Update Product Form
@login_required
def update_product_form_view(request, product_id):
    """AJAX view to load update form in modal"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    form = DynamicProductForm(instance=product)
    
    # Get parent categories (categories with no parent)
    parent_categories = Category.objects.filter(parent__isnull=True)
    
    # Get current category hierarchy for pre-selection
    current_category = product.category
    parent_category = None
    child_category = None
    
    if current_category.parent:
        parent_category = current_category.parent
        child_category = current_category
    else:
        parent_category = current_category
    
    # Get existing attribute values for pre-population
    existing_attributes = {}
    for attr_value in product.attribute_values.all():
        existing_attributes[f'attribute_{attr_value.attribute.id}'] = attr_value.value
    
    context = {
        'form': form,
        'product': product,
        'seller': seller,
        'parent_categories': parent_categories,
        'current_parent_category': parent_category,
        'current_child_category': child_category,
        'existing_attributes': existing_attributes
    }
    return render(request, 'seller/product_form_modal.html', context)


# DELETE Product
@login_required
def delete_product_view(request, product_id):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller:products_list')
    
    context = {
        'product': product,
        'seller': seller
    }
    return render(request, 'seller/product_delete.html', context)


# ========== AJAX VIEWS FOR DYNAMIC FORM ==========

@csrf_exempt
def get_category_children(request):
    """Get child categories for a selected parent category"""
    if request.method == 'POST':
        data = json.loads(request.body)
        parent_id = data.get('parent_id')
        
        if parent_id:
            children = Category.objects.filter(parent_id=parent_id)
            children_data = [{'id': child.id, 'name': child.name} for child in children]
            return JsonResponse({'children': children_data})
        
    return JsonResponse({'children': []})


@csrf_exempt
def get_category_attributes(request):
    """Get attributes for a selected category with existing options"""
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        
        if category_id:
            attributes = CategoryAttribute.objects.filter(category_id=category_id)
            attributes_data = []
            
            for attr in attributes:
                attr_data = {
                    'id': attr.id,
                    'name': attr.name,
                    'input_type': attr.input_type,
                    'is_required': attr.is_required,
                    'unit': attr.unit,
                    'options': []
                }
                
                # Get existing options for all attribute types (not just dropdown)
                options = AttributeOption.objects.filter(attribute=attr)
                attr_data['options'] = [{'id': opt.id, 'value': opt.value} for opt in options]
                
                attributes_data.append(attr_data)
            
            return JsonResponse({'attributes': attributes_data})
    
    return JsonResponse({'attributes': []})


@csrf_exempt
def save_attribute_value(request):
    """Save attribute value and create option if new"""
    if request.method == 'POST':
        data = json.loads(request.body)
        attribute_id = data.get('attribute_id')
        value = data.get('value')
        
        if attribute_id and value:
            try:
                attribute = CategoryAttribute.objects.get(id=attribute_id)
                
                # Check if this value already exists as an option
                existing_option = AttributeOption.objects.filter(
                    attribute=attribute, 
                    value=value
                ).first()
                
                if not existing_option:
                    # Create new option
                    AttributeOption.objects.create(
                        attribute=attribute,
                        value=value
                    )
                
                return JsonResponse({'success': True})
            except CategoryAttribute.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Attribute not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def stripe_onboard(request):
    seller = get_object_or_404(Seller, user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not seller.stripe_account_id:
        # Create a new Stripe account for the seller
        account = stripe.Account.create(
            type="express",
            country="US",
            email=seller.email,
            capabilities={"transfers": {"requested": True}},
        )
        seller.stripe_account_id = account.id
        seller.save()
    # Create an onboarding link
    account_link = stripe.AccountLink.create(
        account=seller.stripe_account_id,
        refresh_url=request.build_absolute_uri('/seller/stripe/refresh/'),
        return_url=request.build_absolute_uri('/seller/dashboard/'),
        type="account_onboarding",
    )
    return redirect(account_link.url)

@login_required
def seller_dashboard(request):
    """Seller dashboard overview with order history and revenue"""
    seller = get_object_or_404(Seller, user=request.user)
    
    # Get all orders for this seller
    orders = Order.objects.filter(seller=seller).order_by('-created_at')
    
    # Calculate revenue statistics
    total_orders = orders.count()
    total_revenue = sum(order.total_amount for order in orders if order.payment_status == 'paid')
    pending_orders = orders.filter(status='pending').count()
    completed_orders = orders.filter(status='delivered').count()
    
    # Recent orders (last 10)
    recent_orders = orders[:10]
    
    context = {
        'seller': seller,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'seller/seller_dashboard.html', context)

@login_required
def seller_orders(request):
    """Detailed order list for seller"""
    seller = get_object_or_404(Seller, user=request.user)
    orders = Order.objects.filter(seller=seller).order_by('-created_at')
    
    context = {
        'seller': seller,
        'orders': orders,
    }
    return render(request, 'seller/orders.html', context)

@login_required
def seller_revenue(request):
    """Revenue and payout tracking for seller"""
    seller = get_object_or_404(Seller, user=request.user)
    
    # Get all paid orders
    paid_orders = Order.objects.filter(seller=seller, payment_status='paid')
    
    # Calculate revenue by month
    from django.db.models import Sum
    from django.db.models.functions import TruncMonth
    
    monthly_revenue = paid_orders.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_amount')
    ).order_by('month')
    
    # Calculate commission (10% of total revenue)
    total_revenue = sum(order.total_amount for order in paid_orders)
    total_commission = total_revenue * 0.10
    net_payout = total_revenue - total_commission
    
    context = {
        'seller': seller,
        'total_revenue': total_revenue,
        'total_commission': total_commission,
        'net_payout': net_payout,
        'monthly_revenue': monthly_revenue,
        'paid_orders': paid_orders,
    }
    return render(request, 'seller/revenue.html', context)

@login_required
def seller_stripe_status(request):
    """Check seller's Stripe onboarding status"""
    seller = get_object_or_404(Seller, user=request.user)
    
    context = {
        'seller': seller,
        'has_stripe': bool(seller.stripe_account_id),
    }
    return render(request, 'seller/stripe_status.html', context)

@login_required
def seller_dashboard_overview(request):
    """Enhanced seller dashboard with comprehensive real data from database"""
    # Allow superuser to select seller by ?seller_id= for debugging
    if request.user.is_superuser and request.GET.get('seller_id'):
        try:
            seller = Seller.objects.get(id=request.GET['seller_id'])
        except Seller.DoesNotExist:
            return HttpResponseBadRequest('Seller not found')
    else:
        seller = get_object_or_404(Seller, user=request.user)

    # Debug logging
    logger = logging.getLogger(__name__)
    logger.info(f"Dashboard for seller ID: {seller.id}, shop: {seller.shop_name}")

    # Get all orders for this seller with detailed information
    all_orders = Order.objects.filter(seller=seller).select_related('buyer').prefetch_related('items__product')
    logger.info(f"Order count: {all_orders.count()}")

    # Get all products for this seller
    products = Product.objects.filter(seller=seller)
    logger.info(f"Product count: {products.count()}")

    # Get recent orders (last 10) with buyer information
    recent_orders = all_orders.order_by('-created_at')[:10]

    # Annotate products for dashboard
    products = products.prefetch_related('images').annotate(
        dashboard_order_count=Count('orderitem__order', distinct=True),
        dashboard_total_sold=Sum('orderitem__quantity'),
        dashboard_total_revenue=Sum('orderitem__price_at_purchase')
    ).order_by('-created_at')

    # Calculate comprehensive statistics
    total_orders = all_orders.count()
    total_products = products.count()

    # Payment method breakdown - use Order model's order_type field
    cod_revenue = all_orders.filter(
        order_type='cod',
        payment_status='paid',
        status='delivered'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    stripe_revenue = all_orders.filter(
        order_type='stripe',
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Total earnings = COD revenue (paid + delivered) + Stripe revenue (paid)
    total_earnings = cod_revenue + stripe_revenue

    # Monthly sales (current month) - COD (paid + delivered) + Stripe (paid)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Monthly COD revenue (paid + delivered orders in current month)
    monthly_cod_revenue = all_orders.filter(
        order_type='cod',
        payment_status='paid',
        status='delivered',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Monthly Stripe revenue (paid orders in current month)
    monthly_stripe_revenue = all_orders.filter(
        order_type='stripe',
        payment_status='paid',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    monthly_sales = monthly_cod_revenue + monthly_stripe_revenue

    # Revenue breakdown by time periods
    weekly_revenue = all_orders.filter(
        payment_status='paid',
        created_at__gte=datetime.now() - timedelta(days=7)
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    monthly_revenue = all_orders.filter(
        payment_status='paid',
        created_at__gte=datetime.now() - timedelta(days=30)
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    yearly_revenue = all_orders.filter(
        payment_status='paid',
        created_at__year=current_year
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Order status breakdown
    pending_orders = all_orders.filter(status='pending').count()
    processing_orders = all_orders.filter(status='processing').count()
    shipped_orders = all_orders.filter(status='shipped').count()
    delivered_orders = all_orders.filter(status='delivered').count()
    cancelled_orders = all_orders.filter(status='cancelled').count()

    # Top selling products with revenue
    top_products = products.annotate(
        dashboard_order_count=Count('orderitem__order', distinct=True),
        dashboard_total_sold=Sum('orderitem__quantity'),
        dashboard_total_revenue=Sum('orderitem__price_at_purchase')
    ).order_by('-dashboard_total_revenue')[:5]

    # Low stock products
    low_stock_products = products.filter(stock__lte=15, stock__gt=0).count()

    # Categories for product forms
    categories = Category.objects.all()

    # Get recent activities from database
    recent_activity = seller.activities.filter(is_cleared=False)[:5]

    # Sales chart data (last 6 months)
    sales_data = []
    for i in range(6):
        month_date = datetime.now() - timedelta(days=30*i)
        month_sales = all_orders.filter(
            payment_status='paid',
            created_at__month=month_date.month,
            created_at__year=month_date.year
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        sales_data.append({
            'month': month_date.strftime('%b'),
            'sales': float(month_sales)
        })
    sales_data.reverse()

    # Get notifications from database
    notifications = seller.notifications.filter(is_read=False)[:10]

    context = {
        'seller': seller,
        'recent_orders': recent_orders,
        'products': products,
        'total_earnings': total_earnings,
        'total_orders': total_orders,
        'total_products': total_products,
        'monthly_sales': monthly_sales,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        'yearly_revenue': yearly_revenue,
        'cod_revenue': cod_revenue,
        'stripe_revenue': stripe_revenue,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'top_products': top_products,
        'low_stock_products': low_stock_products,
        'recent_activity': recent_activity,
        'sales_data': sales_data,
        'categories': categories,
        'notifications': notifications,
    }
    return render(request, 'seller/seller_dashboard.html', context)

@login_required
def seller_orders_list(request):
    """Detailed orders list for seller"""
    seller = get_object_or_404(Seller, user=request.user)
    orders = Order.objects.filter(seller=seller).select_related('buyer').order_by('-created_at')
    
    # Apply search filter
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |
            Q(buyer__name__icontains=search_query) |
            Q(buyer__email__icontains=search_query)
        )
    
    # Apply status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Apply payment status filter
    payment_status_filter = request.GET.get('payment_status', '')
    if payment_status_filter:
        orders = orders.filter(payment_status=payment_status_filter)
    
    # Add pagination
    from django.core.paginator import Paginator
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'seller': seller,
        'orders': page_obj,
        'total_orders': orders.count(),
    }
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the orders table and pagination content
        return render(request, 'seller/orders_list_ajax.html', context)
    
    return render(request, 'seller/orders_list.html', context)

@login_required
def seller_products_list(request):
    """Detailed products list for seller"""
    seller = get_object_or_404(Seller, user=request.user)
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    
    # Add search and filter
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Add pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'seller': seller,
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'seller/products_list.html', context)

@login_required
def seller_add_product(request):
    """Add new product form"""
    seller = get_object_or_404(Seller, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product added successfully!')
            return redirect('seller:products_list')
    else:
        form = ProductForm()
    
    categories = Category.objects.all()
    
    context = {
        'seller': seller,
        'form': form,
        'categories': categories,
    }
    return render(request, 'seller/product_form.html', context)

@login_required
def seller_edit_product(request, product_id):
    """Edit existing product"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            
            # Handle new images
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product updated successfully!')
            return redirect('seller:products_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'seller': seller,
        'product': product,
        'form': form,
    }
    return render(request, 'seller/edit_product.html', context)

@login_required
def seller_delete_product(request, product_id):
    """Delete product"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller:products_list')
    
    context = {
        'seller': seller,
        'product': product,
    }
    return render(request, 'seller/product_delete.html', context)

@login_required
def seller_reports(request):
    """Sales reports and analytics"""
    seller = get_object_or_404(Seller, user=request.user)
    
    # Get orders for this seller
    orders = Order.objects.filter(seller=seller, payment_status='paid')
    
    # Calculate various metrics
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    # Revenue by period
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    
    weekly_revenue = orders.filter(created_at__date__gte=week_ago).aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    monthly_revenue = orders.filter(created_at__date__gte=month_ago).aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    yearly_revenue = orders.filter(created_at__date__gte=year_ago).aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    # Monthly sales data for chart
    monthly_data = []
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_revenue = orders.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        monthly_data.append({
            'month': month_start.strftime('%b'),
            'revenue': month_revenue
        })
    
    monthly_data.reverse()  # Show oldest to newest
    
    # Top selling products with actual sales data
    top_products = Product.objects.filter(seller=seller).annotate(
        total_sold=Sum('orderitem__quantity'),
        total_revenue=Sum('orderitem__price_at_purchase' * 'orderitem__quantity')
    ).order_by('-total_revenue')[:5]
    
    context = {
        'seller': seller,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        'yearly_revenue': yearly_revenue,
        'monthly_data': monthly_data,
        'top_products': top_products,
        'total_orders': orders.count(),
    }
    return render(request, 'seller/reports.html', context)

@login_required
def seller_edit_profile(request):
    """Edit seller profile"""
    seller = get_object_or_404(Seller, user=request.user)
    
    if request.method == 'POST':
        form = SellerUpdateForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('seller:dashboard')
    else:
        form = SellerUpdateForm(instance=seller)
    
    context = {
        'seller': seller,
        'form': form,
    }
    return render(request, 'seller/edit_profile.html', context)

@login_required
@require_POST
def promotion_create(request):
    """Create a new promotion"""
    seller = get_object_or_404(Seller, user=request.user)
    
    try:
        name = request.POST.get('name')
        discount = request.POST.get('discount')
        valid_until_str = request.POST.get('valid_until')
        product_ids = request.POST.getlist('products')
        
        if not name or not discount or not valid_until_str:
            return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
        
        # Parse the valid_until string into a datetime object
        try:
            # Handle different date formats
            if 'T' in valid_until_str:
                # ISO format: "2024-12-31T23:59:59"
                valid_until = timezone.datetime.fromisoformat(valid_until_str.replace('Z', '+00:00'))
            elif len(valid_until_str) == 10:
                # Date-only format: "2024-12-31" (from HTML date input)
                # Set time to end of day (23:59:59)
                valid_until = timezone.datetime.strptime(valid_until_str + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            else:
                # Django format: "2024-12-31 23:59:59"
                valid_until = timezone.datetime.strptime(valid_until_str, '%Y-%m-%d %H:%M:%S')
            
            # Make it timezone-aware if it's not already
            if timezone.is_naive(valid_until):
                valid_until = timezone.make_aware(valid_until)
                
        except ValueError as e:
            return JsonResponse({'success': False, 'error': f'Invalid date format: {valid_until_str}. Expected format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS'})
        
        # Create the promotion with proper valid_from field
        promotion = Promotion.objects.create(
            seller=seller,
            name=name,
            promotion_type='percentage',
            discount_value=float(discount),
            valid_from=timezone.now(),  # Set to current time
            valid_until=valid_until,
            is_active=True
        )
        
        # Add selected products to the promotion
        if product_ids:
            products = Product.objects.filter(id__in=product_ids, seller=seller)
            promotion.products.set(products)
        
        # Create activity for the promotion
        Activity.objects.create(
            seller=seller,
            type='product_updated',
            title=f'Promotion Created: {name}',
            description=f'Created promotion "{name}" with {discount}% discount'
        )
        
        return JsonResponse({
            'success': True, 
            'message': f'Promotion "{name}" created successfully!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def seller_create_promotion(request):
    """Create promotion for products"""
    seller = get_object_or_404(Seller, user=request.user)
    
    if request.method == 'POST':
        # Handle promotion creation
        # This would integrate with a promotion/discount system
        messages.success(request, 'Promotion created successfully!')
        return redirect('seller:dashboard')
    
    products = Product.objects.filter(seller=seller)
    
    context = {
        'seller': seller,
        'products': products,
    }
    return render(request, 'seller/create_promotion.html', context)

@login_required
@require_POST
def export_data(request):
    """Export data in various formats"""
    seller = get_object_or_404(Seller, user=request.user)
    
    try:
        print(f"Export request received for seller: {seller.id}")
        data = json.loads(request.body)
        export_type = data.get('export_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        format_type = data.get('format')
        
        print(f"Export parameters: type={export_type}, format={format_type}, start={start_date}, end={end_date}")
        
        if format_type == 'csv':
            print("Exporting as CSV")
            return export_csv(request, seller, export_type, start_date, end_date)
        elif format_type == 'excel':
            print("Exporting as Excel")
            return export_excel(request, seller, export_type, start_date, end_date)
        elif format_type == 'pdf':
            print("Exporting as PDF")
            return export_pdf(request, seller, export_type, start_date, end_date)
        else:
            print(f"Unsupported format: {format_type}")
            return JsonResponse({'success': False, 'error': 'Format not supported'})
    except Exception as e:
        print(f"Export error: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

def export_csv(request, seller, export_type, start_date, end_date):
    """Export data as CSV"""
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{export_type}_export_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        
        if export_type == 'orders':
            writer.writerow(['Order ID', 'Customer Name', 'Customer Email', 'Total Amount', 'Status', 'Payment Status', 'Order Type', 'Date', 'Delivery Address'])
            orders = Order.objects.filter(seller=seller).select_related('buyer')
            
            # Fix date filtering - only filter if both dates are provided
            if start_date and end_date and start_date.strip() and end_date.strip():
                from datetime import datetime
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                orders = orders.filter(created_at__date__range=[start_dt.date(), end_dt.date()])
            
            for order in orders:
                writer.writerow([
                    order.id,
                    order.buyer.name if hasattr(order.buyer, 'name') else order.buyer.user.username,
                    order.buyer.email,
                    order.total_amount,
                    order.get_status_display(),
                    order.get_payment_status_display(),
                    order.order_type.upper(),
                    order.created_at.strftime('%Y-%m-%d %H:%M'),
                    order.delivery_address or 'N/A'
                ])
        
        elif export_type == 'products':
            writer.writerow(['Product ID', 'Name', 'Category', 'Base Price', 'Final Price', 'Stock', 'Condition', 'Status', 'Created Date'])
            products = Product.objects.filter(seller=seller).select_related('category')
            
            for product in products:
                # Use a simple status based on stock availability instead of is_active
                status = 'Active' if product.stock > 0 else 'Out of Stock'
                writer.writerow([
                    product.id,
                    product.name,
                    product.category.name if product.category else 'Uncategorized',
                    product.base_price,
                    product.final_price,
                    product.stock,
                    product.get_condition_display(),
                    status,
                    product.created_at.strftime('%Y-%m-%d')
                ])
        
        elif export_type == 'sales':
            writer.writerow(['Order ID', 'Product Name', 'Quantity', 'Price at Purchase', 'Total', 'Order Date', 'Status'])
            order_items = OrderItem.objects.filter(order__seller=seller).select_related('order', 'product')
            
            # Fix date filtering for sales
            if start_date and end_date and start_date.strip() and end_date.strip():
                from datetime import datetime
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                order_items = order_items.filter(order__created_at__date__range=[start_dt.date(), end_dt.date()])
            
            for item in order_items:
                writer.writerow([
                    item.order.id,
                    item.product.name,
                    item.quantity,
                    item.price_at_purchase,
                    item.price_at_purchase * item.quantity,
                    item.order.created_at.strftime('%Y-%m-%d'),
                    item.order.get_status_display()
                ])
        
        elif export_type == 'inventory':
            writer.writerow(['Product ID', 'Name', 'Category', 'Current Stock', 'Low Stock Alert', 'Total Sold', 'Revenue Generated', 'Last Updated'])
            products = Product.objects.filter(seller=seller).select_related('category')
            
            for product in products:
                low_stock = 'Yes' if product.stock <= 15 else 'No'
                
                # Calculate totals manually to avoid type issues
                order_items = OrderItem.objects.filter(product=product)
                total_sold = sum(item.quantity for item in order_items)
                revenue_generated = sum(item.price_at_purchase * item.quantity for item in order_items)
                
                writer.writerow([
                    product.id,
                    product.name,
                    product.category.name if product.category else 'Uncategorized',
                    product.stock,
                    low_stock,
                    total_sold,
                    revenue_generated,
                    product.created_at.strftime('%Y-%m-%d %H:%M')
                ])
        
        return response
    except Exception as e:
        print(f"CSV export error: {str(e)}")
        return JsonResponse({'success': False, 'error': f'CSV export failed: {str(e)}'})

def export_excel(request, seller, export_type, start_date, end_date):
    """Export data as Excel"""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        return JsonResponse({'success': False, 'error': 'Excel export requires openpyxl package'})
    
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = export_type.title()
        
        # Style for headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        if export_type == 'orders':
            headers = ['Order ID', 'Customer Name', 'Customer Email', 'Total Amount', 'Status', 'Payment Status', 'Order Type', 'Date', 'Delivery Address']
            ws.append(headers)
            
            # Style headers
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            orders = Order.objects.filter(seller=seller).select_related('buyer')
            
            # Fix date filtering - only filter if both dates are provided
            if start_date and end_date and start_date.strip() and end_date.strip():
                from datetime import datetime
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                orders = orders.filter(created_at__date__range=[start_dt.date(), end_dt.date()])
            
            for order in orders:
                ws.append([
                    order.id,
                    order.buyer.name if hasattr(order.buyer, 'name') else order.buyer.user.username,
                    order.buyer.email,
                    order.total_amount,
                    order.get_status_display(),
                    order.get_payment_status_display(),
                    order.order_type.upper(),
                    order.created_at.strftime('%Y-%m-%d %H:%M'),
                    order.delivery_address or 'N/A'
                ])
        
        elif export_type == 'products':
            headers = ['Product ID', 'Name', 'Category', 'Base Price', 'Final Price', 'Stock', 'Condition', 'Status', 'Created Date']
            ws.append(headers)
            
            # Style headers
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            products = Product.objects.filter(seller=seller).select_related('category')
            
            for product in products:
                # Use a simple status based on stock availability instead of is_active
                status = 'Active' if product.stock > 0 else 'Out of Stock'
                ws.append([
                    product.id,
                    product.name,
                    product.category.name if product.category else 'Uncategorized',
                    product.base_price,
                    product.final_price,
                    product.stock,
                    product.get_condition_display(),
                    status,
                    product.created_at.strftime('%Y-%m-%d')
                ])
        
        elif export_type == 'sales':
            headers = ['Order ID', 'Product Name', 'Quantity', 'Price at Purchase', 'Total', 'Order Date', 'Status']
            ws.append(headers)
            
            # Style headers
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            order_items = OrderItem.objects.filter(order__seller=seller).select_related('order', 'product')
            
            # Fix date filtering for sales
            if start_date and end_date and start_date.strip() and end_date.strip():
                from datetime import datetime
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                order_items = order_items.filter(order__created_at__date__range=[start_dt.date(), end_dt.date()])
            
            for item in order_items:
                ws.append([
                    item.order.id,
                    item.product.name,
                    item.quantity,
                    item.price_at_purchase,
                    item.price_at_purchase * item.quantity,
                    item.order.created_at.strftime('%Y-%m-%d'),
                    item.order.get_status_display()
                ])
        
        elif export_type == 'inventory':
            headers = ['Product ID', 'Name', 'Category', 'Current Stock', 'Low Stock Alert', 'Total Sold', 'Revenue Generated', 'Last Updated']
            ws.append(headers)
            
            # Style headers
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            products = Product.objects.filter(seller=seller).select_related('category')
            
            for product in products:
                low_stock = 'Yes' if product.stock <= 15 else 'No'
                
                # Calculate totals manually to avoid type issues
                order_items = OrderItem.objects.filter(product=product)
                total_sold = sum(item.quantity for item in order_items)
                revenue_generated = sum(item.price_at_purchase * item.quantity for item in order_items)
                
                ws.append([
                    product.id,
                    product.name,
                    product.category.name if product.category else 'Uncategorized',
                    product.stock,
                    low_stock,
                    total_sold,
                    revenue_generated,
                    product.created_at.strftime('%Y-%m-%d %H:%M')
                ])
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{export_type}_export_{timezone.now().strftime("%Y%m%d")}.xlsx"'
        wb.save(response)
        return response
        
    except Exception as e:
        print(f"Excel export error: {str(e)}")
        return JsonResponse({'success': False, 'error': f'Excel export failed: {str(e)}'})

def export_pdf(request, seller, export_type, start_date, end_date):
    """Export data as PDF"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
    except ImportError:
        return JsonResponse({'success': False, 'error': 'PDF export requires reportlab package'})
    
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{export_type}_export_{timezone.now().strftime("%Y%m%d")}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        
        # Title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        title = Paragraph(f"{export_type.title()} Report - {seller.shop_name}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        if export_type == 'orders':
            headers = ['Order ID', 'Customer', 'Total', 'Status', 'Payment', 'Type', 'Date']
            data = [headers]
            
            orders = Order.objects.filter(seller=seller).select_related('buyer')
            
            # Fix date filtering - only filter if both dates are provided
            if start_date and end_date and start_date.strip() and end_date.strip():
                from datetime import datetime
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                orders = orders.filter(created_at__date__range=[start_dt.date(), end_dt.date()])
            
            for order in orders:
                data.append([
                    str(order.id),
                    order.buyer.name if hasattr(order.buyer, 'name') else order.buyer.user.username,
                    f"${order.total_amount}",
                    order.get_status_display(),
                    order.get_payment_status_display(),
                    order.order_type.upper(),
                    order.created_at.strftime('%Y-%m-%d')
                ])
        
        elif export_type == 'products':
            headers = ['Product ID', 'Name', 'Category', 'Price', 'Stock', 'Status']
            data = [headers]
            
            products = Product.objects.filter(seller=seller).select_related('category')
            
            for product in products:
                # Use a simple status based on stock availability instead of is_active
                status = 'Active' if product.stock > 0 else 'Out of Stock'
                data.append([
                    str(product.id),
                    product.name,
                    product.category.name if product.category else 'Uncategorized',
                    f"${product.final_price}",
                    str(product.stock),
                    status
                ])
        
        elif export_type == 'sales':
            headers = ['Order ID', 'Product', 'Quantity', 'Price', 'Total', 'Date']
            data = [headers]
            
            order_items = OrderItem.objects.filter(order__seller=seller).select_related('order', 'product')
            
            # Fix date filtering for sales
            if start_date and end_date and start_date.strip() and end_date.strip():
                from datetime import datetime
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                order_items = order_items.filter(order__created_at__date__range=[start_dt.date(), end_dt.date()])
            
            for item in order_items:
                data.append([
                    str(item.order.id),
                    item.product.name,
                    str(item.quantity),
                    f"${item.price_at_purchase}",
                    f"${item.price_at_purchase * item.quantity}",
                    item.order.created_at.strftime('%Y-%m-%d')
                ])
        
        elif export_type == 'inventory':
            headers = ['Product ID', 'Name', 'Stock', 'Low Stock', 'Total Sold', 'Revenue']
            data = [headers]
            
            products = Product.objects.filter(seller=seller).select_related('category')
            
            for product in products:
                low_stock = 'Yes' if product.stock <= 15 else 'No'
                
                # Calculate totals manually to avoid type issues
                order_items = OrderItem.objects.filter(product=product)
                total_sold = sum(item.quantity for item in order_items)
                revenue_generated = sum(item.price_at_purchase * item.quantity for item in order_items)
                
                data.append([
                    str(product.id),
                    product.name,
                    str(product.stock),
                    low_stock,
                    str(total_sold),
                    f"${revenue_generated}"
                ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        return response
        
    except Exception as e:
        print(f"PDF export error: {str(e)}")
        return JsonResponse({'success': False, 'error': f'PDF export failed: {str(e)}'})

@login_required
@require_GET
def check_new_orders(request):
    """Check for new orders (for real-time notifications)"""
    seller = get_object_or_404(Seller, user=request.user)
    
    # Check for orders created in the last 5 minutes
    recent_orders = Order.objects.filter(
        seller=seller,
        created_at__gte=datetime.now() - timedelta(minutes=5)
    ).count()
    
    return JsonResponse({'new_orders': recent_orders})

@login_required
@require_GET
def check_low_stock(request):
    """Check for products with low stock"""
    seller = get_object_or_404(Seller, user=request.user)
    
    low_stock_products = Product.objects.filter(
        seller=seller,
        stock__lte=15,
        stock__gt=0
    ).count()
    
    return JsonResponse({'low_stock_products': low_stock_products})

def calculate_seller_stats(seller):
    """Calculate seller statistics for dashboard"""
    from datetime import datetime, timedelta
    
    # Get current month
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # COD revenue (paid COD orders that are delivered)
    cod_revenue = Order.objects.filter(
        seller=seller,
        order_type='cod',
        payment_status='paid',
        status='delivered'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Stripe revenue (paid Stripe orders)
    stripe_revenue = Order.objects.filter(
        seller=seller,
        order_type='stripe',
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Total earnings = COD revenue + Stripe revenue
    total_earnings = cod_revenue + stripe_revenue
    
    # Monthly sales (current month) - COD (paid + delivered) + Stripe (paid)
    monthly_cod_revenue = Order.objects.filter(
        seller=seller,
        order_type='cod',
        payment_status='paid',
        status='delivered',
        created_at__gte=start_of_month
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    monthly_stripe_revenue = Order.objects.filter(
        seller=seller,
        order_type='stripe',
        payment_status='paid',
        created_at__gte=start_of_month
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    monthly_sales = monthly_cod_revenue + monthly_stripe_revenue
    
    return {
        'total_earnings': total_earnings,
        'monthly_sales': monthly_sales,
        'cod_revenue': cod_revenue,
        'stripe_revenue': stripe_revenue
    }

@login_required
@require_POST
def mark_notification_as_read(request):
    """Mark a specific notification as read"""
    try:
        notification_id = request.POST.get('notification_id')
        seller = get_object_or_404(Seller, user=request.user)
        
        notification = get_object_or_404(Notification, id=notification_id, seller=seller)
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'success': True, 'message': 'Notification marked as read'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@login_required
@require_POST
def mark_all_notifications_as_read(request):
    """Mark all notifications as read for a seller"""
    try:
        seller = get_object_or_404(Seller, user=request.user)
        
        # Mark all unread notifications as read
        updated_count = seller.notifications.filter(is_read=False).update(is_read=True)
        
        return JsonResponse({
            'success': True, 
            'message': f'{updated_count} notifications marked as read'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@login_required
@require_POST
def clear_all_notifications(request):
    """Delete all notifications for a seller"""
    try:
        seller = get_object_or_404(Seller, user=request.user)
        
        # Delete all notifications
        deleted_count = seller.notifications.count()
        seller.notifications.all().delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'{deleted_count} notifications cleared'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@login_required
@require_POST
def clear_all_activity(request):
    """Clear all activities for a seller"""
    try:
        seller = get_object_or_404(Seller, user=request.user)
        
        # Mark all activities as cleared
        updated_count = seller.activities.filter(is_cleared=False).update(is_cleared=True)
        
        return JsonResponse({
            'success': True, 
            'message': f'{updated_count} activities cleared'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@login_required
@require_POST
def mark_activity_as_cleared(request):
    """Mark a specific activity as cleared"""
    try:
        activity_id = request.POST.get('activity_id')
        seller = get_object_or_404(Seller, user=request.user)
        
        activity = get_object_or_404(Activity, id=activity_id, seller=seller)
        activity.is_cleared = True
        activity.save()
        
        return JsonResponse({'success': True, 'message': 'Activity marked as cleared'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

# ========== HOT OFFERS FEATURE ==========

def hot_offers_view(request):
    """Display all active promotions across the platform"""
    from django.db.models import Q
    from django.utils import timezone
    
    # Get all active promotions
    active_promotions = Promotion.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_until__gte=timezone.now()
    ).select_related('seller').prefetch_related('products', 'categories')
    
    # Debug: Print promotion dates
    print("=== DEBUG: Active Promotions ===")
    for promo in active_promotions:
        print(f"Promotion: {promo.name}")
        print(f"  valid_from: {promo.valid_from}")
        print(f"  valid_until: {promo.valid_until}")
        print(f"  is_active: {promo.is_active}")
        print(f"  now: {timezone.now()}")
        print(f"  valid_from <= now: {promo.valid_from <= timezone.now()}")
        print(f"  valid_until >= now: {promo.valid_until >= timezone.now()}")
        print("---")
    
    # Get all categories for filtering
    categories = Category.objects.all()
    
    # Handle search and filtering
    search_query = request.GET.get('search', '')
    category_filter = request.GET.getlist('category')
    
    if search_query:
        active_promotions = active_promotions.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(seller__shop_name__icontains=search_query) |
            Q(products__name__icontains=search_query)
        ).distinct()
    
    if category_filter:
        active_promotions = active_promotions.filter(
            Q(categories__id__in=category_filter) |
            Q(products__category__id__in=category_filter)
        ).distinct()
    
    # Get user info for context
    user = request.user if request.user.is_authenticated else None
    seller = None
    buyer = None
    user_type = None
    
    if user:
        try:
            seller = Seller.objects.get(user=user)
            user_type = 'seller'
        except Seller.DoesNotExist:
            try:
                buyer = Buyer.objects.get(email=user.email)
                user_type = 'buyer'
            except Buyer.DoesNotExist:
                pass
    
    context = {
        'promotions': active_promotions,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'user': user,
        'seller': seller,
        'buyer': buyer,
        'user_type': user_type,
    }
    
    return render(request, 'seller/hot_offers.html', context)

def promotion_detail_view(request, promotion_id):
    """Display detailed information about a specific promotion"""
    promotion = get_object_or_404(Promotion, id=promotion_id)
    
    # Get user info for context
    user = request.user if request.user.is_authenticated else None
    seller = None
    buyer = None
    user_type = None
    
    if user:
        try:
            seller = Seller.objects.get(user=user)
            user_type = 'seller'
        except Seller.DoesNotExist:
            try:
                buyer = Buyer.objects.get(email=user.email)
                user_type = 'buyer'
            except Buyer.DoesNotExist:
                pass
    
    # Get products in this promotion
    promotion_products = promotion.products.all().prefetch_related('images', 'category')
    
    # Calculate time remaining
    from django.utils import timezone
    now = timezone.now()
    time_remaining = promotion.valid_until - now
    
    context = {
        'promotion': promotion,
        'promotion_products': promotion_products,
        'time_remaining': time_remaining,
        'user': user,
        'seller': seller,
        'buyer': buyer,
        'user_type': user_type,
    }
    
    return render(request, 'seller/promotion_detail.html', context)

def search_promotions_ajax(request):
    """AJAX endpoint for searching promotions"""
    from django.db.models import Q
    from django.utils import timezone
    
    search_query = request.GET.get('q', '')
    category_filter = request.GET.getlist('category')
    
    # Get active promotions
    promotions = Promotion.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_until__gte=timezone.now()
    ).select_related('seller').prefetch_related('products', 'categories')
    
    # Apply search filter
    if search_query:
        promotions = promotions.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(seller__shop_name__icontains=search_query) |
            Q(products__name__icontains=search_query)
        ).distinct()
    
    # Apply category filter
    if category_filter:
        promotions = promotions.filter(
            Q(categories__id__in=category_filter) |
            Q(products__category__id__in=category_filter)
        ).distinct()
    
    # Serialize promotions for JSON response
    promotions_data = []
    for promotion in promotions:
        promotion_data = {
            'id': promotion.id,
            'name': promotion.name,
            'description': promotion.description,
            'promotion_type': promotion.promotion_type,
            'discount_value': promotion.discount_value,
            'seller_name': promotion.seller.shop_name,
            'valid_until': promotion.valid_until.isoformat(),
            'products_count': promotion.products.count(),
            'url': f'/promotion/{promotion.id}/'
        }
        promotions_data.append(promotion_data)
    
    return JsonResponse({'promotions': promotions_data})

def get_active_promotions_for_homepage():
    """Get active promotions for homepage display - 5 trending promotions ordered by expiration"""
    from django.utils import timezone
    
    # Get 5 active promotions ordered by expiration date (soonest first)
    promotions = Promotion.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_until__gte=timezone.now()
    ).select_related('seller').prefetch_related('products').order_by('valid_until')[:5]
    
    return promotions

@login_required
def seller_export_data(request):
    """Handle export data requests"""
    seller = get_object_or_404(Seller, user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            export_type = data.get('export_type')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            format_type = data.get('format')
            
            if format_type == 'csv':
                return export_csv(request, seller, export_type, start_date, end_date)
            elif format_type == 'excel':
                return export_excel(request, seller, export_type, start_date, end_date)
            elif format_type == 'pdf':
                return export_pdf(request, seller, export_type, start_date, end_date)
            else:
                return JsonResponse({'success': False, 'error': 'Format not supported'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def test_export(request):
    """Test export functionality"""
    seller = get_object_or_404(Seller, user=request.user)
    
    # Test CSV export
    try:
        csv_response = export_csv(request, seller, 'products', None, None)
        print("CSV export test successful")
    except Exception as e:
        print(f"CSV export test failed: {e}")
    
    # Test Excel export
    try:
        excel_response = export_excel(request, seller, 'products', None, None)
        print("Excel export test successful")
    except Exception as e:
        print(f"Excel export test failed: {e}")
    
    # Test PDF export
    try:
        pdf_response = export_pdf(request, seller, 'products', None, None)
        print("PDF export test successful")
    except Exception as e:
        print(f"PDF export test failed: {e}")
    
    return JsonResponse({'success': True, 'message': 'Export tests completed'})

@login_required
def simple_export_test(request):
    """Simple test to verify export works"""
    seller = get_object_or_404(Seller, user=request.user)
    
    try:
        # Create a simple CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="test_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Test', 'Data'])
        writer.writerow(['Product', 'Test Product'])
        writer.writerow(['Price', '100'])
        
        print("Simple export test successful")
        return response
        
    except Exception as e:
        print(f"Simple export test failed: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

# Missing functions that are referenced in URLs
@login_required
def product_edit_data(request, product_id):
    """Get product data for editing"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    context = {
        'product': product,
        'seller': seller,
    }
    return render(request, 'seller/product_edit_data.html', context)

@login_required
@require_POST
def product_update(request, product_id):
    """Update product data"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    try:
        # Update basic fields
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.base_price = float(request.POST.get('base_price', product.base_price))
        product.stock = int(request.POST.get('stock', product.stock))
        product.condition = request.POST.get('condition', product.condition)
        
        # Update final price if discount is provided
        discount = request.POST.get('discount_percentage')
        if discount:
            product.discount_percentage = float(discount)
            product.final_price = product.base_price * (1 - float(discount) / 100)
        else:
            product.final_price = product.base_price
        
        product.save()
        
        return JsonResponse({'success': True, 'message': 'Product updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def product_delete(request, product_id):
    """Delete product"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    try:
        product_name = product.name
        product.delete()
        return JsonResponse({'success': True, 'message': f'Product "{product_name}" deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def product_duplicate(request, product_id):
    """Duplicate product"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    try:
        # Create a copy of the product
        new_product = Product.objects.create(
            seller=seller,
            category=product.category,
            brand=product.brand,
            name=f"{product.name} (Copy)",
            description=product.description,
            base_price=product.base_price,
            discount_percentage=product.discount_percentage,
            final_price=product.final_price,
            stock=product.stock,
            condition=product.condition,
            rating_avg=product.rating_avg,
            order_count=0
        )
        
        # Copy images
        for image in product.images.all():
            ProductImage.objects.create(
                product=new_product,
                image=image.image,
                is_thumbnail=image.is_thumbnail
            )
        
        # Copy attribute values
        for attr_value in product.attribute_values.all():
            ProductAttributeValue.objects.create(
                product=new_product,
                attribute=attr_value.attribute,
                value=attr_value.value
            )
        
        return JsonResponse({
            'success': True, 
            'message': f'Product "{product.name}" duplicated successfully',
            'new_product_id': new_product.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def order_details(request, order_id):
    """Get order details"""
    seller = get_object_or_404(Seller, user=request.user)
    order = get_object_or_404(Order, id=order_id, seller=seller)
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'id': order.id,
            'customer_name': order.buyer.name if hasattr(order.buyer, 'name') else order.buyer.user.username,
            'customer_email': order.buyer.email,
            'order_type': order.order_type,
            'status': order.status,
            'payment_status': order.payment_status,
            'total_amount': order.total_amount,
            'tracking_number': order.tracking_number or '',
            'notes': order.notes or '',
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'delivery_address': order.delivery_address or 'N/A'
        })
    
    context = {
        'order': order,
        'seller': seller,
    }
    return render(request, 'seller/order_details.html', context)

@login_required
@require_POST
def order_update_status(request):
    """Update order status"""
    seller = get_object_or_404(Seller, user=request.user)
    
    try:
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        payment_status = request.POST.get('payment_status')
        tracking_number = request.POST.get('tracking_number')
        notes = request.POST.get('notes')
        
        order = get_object_or_404(Order, id=order_id, seller=seller)
        
        # Track what was updated
        updates_made = []
        
        # Update order status
        if new_status and new_status != order.status:
            order.status = new_status
            updates_made.append(f'Status: {new_status}')
        
        # Update payment status if provided
        if payment_status and payment_status != order.payment_status:
            order.payment_status = payment_status
            updates_made.append(f'Payment: {payment_status}')
        
        # Update tracking number if provided
        if tracking_number and tracking_number != order.tracking_number:
            order.tracking_number = tracking_number
            updates_made.append(f'Tracking: {tracking_number}')
        
        # Update notes if provided
        if notes and notes != order.notes:
            order.notes = notes
            updates_made.append('Notes updated')
        
        order.save()
        
        # Create activity for status update
        if updates_made:
            Activity.objects.create(
                seller=seller,
                type='order_updated',
                title=f'Order #{order_id} Updated',
                description=f'Updated: {", ".join(updates_made)}'
            )
        
        # Calculate updated stats for dashboard
        updated_stats = calculate_seller_stats(seller)
        
        return JsonResponse({
            'success': True, 
            'message': f'Order #{order_id} updated successfully',
            'order_type': order.order_type,
            'payment_updated': payment_status and payment_status != order.payment_status,
            'updated_stats': updated_stats
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def test_create_promotion(request):
    """Test function to create a promotion with correct dates"""
    from datetime import timedelta
    
    seller = get_object_or_404(Seller, user=request.user)
    
    # Create a test promotion that expires in 30 days
    now = timezone.now()
    valid_until = now + timedelta(days=30)
    
    promotion = Promotion.objects.create(
        seller=seller,
        name="Test Countdown Promotion",
        description="Testing countdown functionality",
        promotion_type='percentage',
        discount_value=20.0,
        valid_from=now,
        valid_until=valid_until,
        is_active=True
    )
    
    return JsonResponse({
        'success': True,
        'message': f'Test promotion created with valid_until: {valid_until}',
        'promotion_id': promotion.id
    })
