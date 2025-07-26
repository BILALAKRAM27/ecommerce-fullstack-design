import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Seller, Product, ProductImage, Brand, Category, CategoryAttribute, AttributeOption, ProductAttributeValue
from .forms import UserRegisterForm, SellerUpdateForm, SellerLoginForm, ProductForm, ProductImageForm, DynamicProductForm
from django.utils import timezone
from buyer.models import Buyer, Order, OrderStatus, Payment
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
    total_earnings = all_orders.filter(payment_status='paid').aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_orders = all_orders.count()
    total_products = products.count()

    # Payment method breakdown - need to check Payment model for actual payment method
    cod_revenue = 0
    stripe_revenue = 0

    # Get payments for this seller's orders
    payments = Payment.objects.filter(order__seller=seller, status='paid')
    for payment in payments:
        if payment.payment_method == 'cash_on_delivery':
            cod_revenue += payment.order.total_amount
        elif payment.payment_method == 'stripe':
            stripe_revenue += payment.order.total_amount

    # Monthly sales (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_sales = all_orders.filter(
        payment_status='paid',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total=Sum('total_amount'))['total'] or 0

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
    low_stock_products = products.filter(stock__lte=5, stock__gt=0).count()

    # Categories for product forms
    categories = Category.objects.all()

    # Recent activity (last 5 orders with details)
    recent_activity = all_orders.select_related('buyer').prefetch_related('items__product')[:5]

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

    notifications = [
        {
            'type': 'order',
            'title': f'New Order Received',
            'message': f'You have {pending_orders} pending orders',
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'type': 'stock',
            'title': 'Low Stock Alert',
            'message': f'{low_stock_products} products are running low on stock',
            'created_at': datetime.now() - timedelta(hours=5)
        }
    ]

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
def seller_export_data(request):
    """Export seller data"""
    seller = get_object_or_404(Seller, user=request.user)
    export_type = request.GET.get('type', 'orders')
    
    if export_type == 'orders':
        data = Order.objects.filter(seller=seller)
        filename = f'orders_export_{seller.shop_name}_{timezone.now().strftime("%Y%m%d")}.csv'
    elif export_type == 'products':
        data = Product.objects.filter(seller=seller)
        filename = f'products_export_{seller.shop_name}_{timezone.now().strftime("%Y%m%d")}.csv'
    else:
        messages.error(request, 'Invalid export type')
        return redirect('seller:dashboard')
    
    # Create CSV response
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
    if export_type == 'orders':
        writer.writerow(['Order ID', 'Customer', 'Total', 'Status', 'Date'])
        for order in data:
            writer.writerow([
                order.id,
                f"{order.buyer.first_name} {order.buyer.last_name}",
                order.total_amount,
                order.get_status_display(),
                order.created_at.strftime('%Y-%m-%d')
            ])
    elif export_type == 'products':
        writer.writerow(['Product Name', 'Price', 'Category', 'Status'])
        for product in data:
            writer.writerow([
                product.name,
                product.final_price,
                product.category.name if product.category else 'N/A',
                'Active' if product.is_active else 'Inactive'
            ])
    
    return response

@login_required
@require_GET
def product_edit_data(request, product_id):
    """Get product data for editing"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    data = {
        'id': product.id,
        'name': product.name,
        'price': float(product.final_price),
        'stock': product.stock,
        'category': product.category.id if product.category else None,
        'description': product.description,
        'is_active': product.is_active,
    }
    
    return JsonResponse(data)

@login_required
@require_POST
def product_update(request, product_id):
    """Update product information"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    # Debug: Print POST data
    print(f"POST data: {request.POST}")
    print(f"FILES data: {request.FILES}")
    
    try:
        # Update basic fields
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.condition = request.POST.get('condition', product.condition)
        
        # Update pricing
        base_price = request.POST.get('base_price')
        if base_price:
            product.base_price = float(base_price)
        
        discount_percentage = request.POST.get('discount_percentage')
        if discount_percentage:
            product.discount_percentage = float(discount_percentage)
            # Calculate final price
            if product.base_price and product.discount_percentage:
                product.final_price = product.base_price * (1 - product.discount_percentage / 100)
        else:
            product.discount_percentage = 0
            product.final_price = product.base_price
        
        # Update stock
        stock = request.POST.get('stock')
        if stock:
            product.stock = int(stock)
        
        # Update category
        category_id = request.POST.get('category')
        if category_id:
            try:
                product.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        
        # Update brand
        brand_id = request.POST.get('brand')
        if brand_id:
            try:
                product.brand = Brand.objects.get(id=brand_id)
            except Brand.DoesNotExist:
                pass
        
        # Handle images
        if 'image_file' in request.FILES:
            image_mode = request.POST.get('image_mode', 'add')
            files = request.FILES.getlist('image_file')
            
            if image_mode == 'replace':
                # Delete existing images and replace with new ones
                product.images.all().delete()
                
                for i, file in enumerate(files):
                    image_data = file.read()
                    ProductImage.objects.create(
                        product=product,
                        image=image_data,
                        is_thumbnail=(i == 0)  # First new image becomes thumbnail
                    )
            else:  # 'add' mode
                # Keep existing images and add new ones
                existing_count = product.images.count()
                
                for i, file in enumerate(files):
                    image_data = file.read()
                    ProductImage.objects.create(
                        product=product,
                        image=image_data,
                        is_thumbnail=(existing_count == 0 and i == 0)  # Only thumbnail if no existing images
                    )
        
        # Handle thumbnail selection
        existing_thumbnail_id = request.POST.get('existing_thumbnail')
        new_thumbnail_index = request.POST.get('new_thumbnail')
        
        if existing_thumbnail_id:
            # Reset all existing images to not be thumbnail
            product.images.all().update(is_thumbnail=False)
            # Set the selected existing image as thumbnail
            try:
                selected_image = ProductImage.objects.get(id=existing_thumbnail_id, product=product)
                selected_image.is_thumbnail = True
                selected_image.save()
            except ProductImage.DoesNotExist:
                pass
        elif new_thumbnail_index is not None and 'image_file' in request.FILES:
            # Set the selected new image as thumbnail
            try:
                new_thumbnail_index = int(new_thumbnail_index)
                # Find the newly created image at the specified index
                new_images = ProductImage.objects.filter(product=product).order_by('-id')[:len(request.FILES.getlist('image_file'))]
                if new_thumbnail_index < len(new_images):
                    # Reset all images to not be thumbnail
                    product.images.all().update(is_thumbnail=False)
                    # Set the selected new image as thumbnail
                    new_images[new_thumbnail_index].is_thumbnail = True
                    new_images[new_thumbnail_index].save()
            except (ValueError, IndexError):
                pass
        
        # Handle attribute values
        for key, value in request.POST.items():
            if key.startswith('attribute_'):
                attr_id = key.replace('attribute_', '')
                try:
                    attr = CategoryAttribute.objects.get(id=attr_id)
                    # Update or create attribute value
                    attr_value, created = ProductAttributeValue.objects.get_or_create(
                        product=product,
                        attribute=attr,
                        defaults={'value': value}
                    )
                    if not created:
                        attr_value.value = value
                        attr_value.save()
                except CategoryAttribute.DoesNotExist:
                    pass
        
        product.save()
        
        # Update product order count if needed
        if not hasattr(product, 'order_count'):
            product.order_count = 0
            product.save()
        
        return JsonResponse({'success': True, 'message': 'Product updated successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def product_delete(request, product_id):
    """Delete a product"""
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    try:
        product.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def product_duplicate(request, product_id):
    """Duplicate a product"""
    seller = get_object_or_404(Seller, user=request.user)
    original_product = get_object_or_404(Product, id=product_id, seller=seller)
    
    try:
        # Create a copy of the product
        new_product = Product.objects.create(
            seller=seller,
            name=f"{original_product.name} (Copy)",
            final_price=original_product.final_price,
            stock=original_product.stock,
            description=original_product.description,
            category=original_product.category,
            is_active=False  # Start as inactive
        )
        
        # Copy images if any
        for image in original_product.images.all():
            ProductImage.objects.create(
                product=new_product,
                image=image.image,
                is_thumbnail=image.is_thumbnail
            )
        
        return JsonResponse({'success': True, 'product_id': new_product.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_GET
def order_details(request, order_id):
    """Get detailed order information"""
    seller = get_object_or_404(Seller, user=request.user)
    order = get_object_or_404(Order, id=order_id, seller=seller)
    
    # Get order items
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    
    # Get payment information
    payment_info = None
    try:
        payment = Payment.objects.get(order=order)
        payment_info = {
            'method': payment.get_payment_method_display(),
            'transaction_id': payment.transaction_id,
            'status': payment.get_status_display(),
            'payment_time': payment.payment_time.isoformat() if payment.payment_time else None,
        }
    except Payment.DoesNotExist:
        payment_info = {
            'method': 'Not specified',
            'transaction_id': 'N/A',
            'status': order.get_payment_status_display(),
            'payment_time': None,
        }
    
    data = {
        'id': order.id,
        'created_at': order.created_at.isoformat(),
        'status': order.status,
        'payment_status': order.payment_status,
        'order_type': order.order_type,
        'total_amount': float(order.total_amount),
        'delivery_address': order.delivery_address,
        'tracking_number': order.tracking_number or 'Not provided',
        'notes': order.notes or 'No notes',
        'get_status_display': order.get_status_display(),
        'get_payment_status_display': order.get_payment_status_display(),
        'buyer': {
            'name': order.buyer.display_name,
            'email': order.buyer.email,
            'phone': order.buyer.phone or 'N/A',
        },
        'payment': payment_info,
        'items': [
            {
                'product': {
                    'name': item.product.name,
                    'id': item.product.id,
                },
                'quantity': item.quantity,
                'price_at_purchase': float(item.price_at_purchase),
                'total': float(item.price_at_purchase * item.quantity),
            }
            for item in order_items
        ]
    }
    
    return JsonResponse(data)

@login_required
@require_POST
def order_update_status(request):
    """Update order status"""
    seller = get_object_or_404(Seller, user=request.user)
    order_id = request.POST.get('order_id')
    new_status = request.POST.get('status')
    tracking_number = request.POST.get('tracking_number', '')
    notes = request.POST.get('notes', '')
    
    if not order_id or not new_status:
        return JsonResponse({'success': False, 'error': 'Order ID and status are required'})
    
    try:
        order = get_object_or_404(Order, id=order_id, seller=seller)
        
        # Validate status
        valid_statuses = [choice[0] for choice in OrderStatus.choices]
        if new_status not in valid_statuses:
            return JsonResponse({'success': False, 'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'})
        
        order.status = new_status
        
        # Store tracking number and notes
        if tracking_number:
            order.tracking_number = tracking_number
        if notes:
            order.notes = notes
            
        order.save()
        return JsonResponse({'success': True, 'message': f'Order status updated to {order.get_status_display()}'})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def promotion_create(request):
    """Create a new promotion"""
    seller = get_object_or_404(Seller, user=request.user)
    
    try:
        name = request.POST.get('name')
        discount = request.POST.get('discount')
        valid_until = request.POST.get('valid_until')
        product_ids = request.POST.getlist('products')
        
        # In a real implementation, you would create a Promotion model
        # For now, we'll just return success
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def export_data(request):
    """Export data in various formats"""
    seller = get_object_or_404(Seller, user=request.user)
    
    try:
        data = json.loads(request.body)
        export_type = data.get('export_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        format_type = data.get('format')
        
        if format_type == 'csv':
            return export_csv(request, seller, export_type, start_date, end_date)
        else:
            return JsonResponse({'success': False, 'error': 'Format not supported'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def export_csv(request, seller, export_type, start_date, end_date):
    """Export data as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{export_type}_export.csv"'
    
    writer = csv.writer(response)
    
    if export_type == 'orders':
        writer.writerow(['Order ID', 'Customer', 'Total', 'Status', 'Date'])
        orders = Order.objects.filter(seller=seller)
        if start_date and end_date:
            orders = orders.filter(created_at__range=[start_date, end_date])
        
        for order in orders:
            writer.writerow([
                order.id,
                order.buyer.name if hasattr(order.buyer, 'name') else order.buyer.user.username,
                order.total_amount,
                order.get_status_display(),
                order.created_at.strftime('%Y-%m-%d')
            ])
    
    elif export_type == 'products':
        writer.writerow(['Product ID', 'Name', 'Price', 'Stock', 'Status'])
        products = Product.objects.filter(seller=seller)
        
        for product in products:
            writer.writerow([
                product.id,
                product.name,
                product.final_price,
                product.stock,
                'Active' if product.is_active else 'Inactive'
            ])
    
    return response

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
        stock__lte=5,
        stock__gt=0
    ).count()
    
    return JsonResponse({'low_stock_products': low_stock_products})
