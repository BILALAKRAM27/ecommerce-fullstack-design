import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Seller, Product, ProductImage, Brand, Category, CategoryAttribute, AttributeOption
from .forms import UserRegisterForm, SellerUpdateForm, SellerLoginForm, ProductForm, ProductImageForm, DynamicProductForm
from django.utils import timezone
from buyer.models import Buyer, Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import stripe
from django.conf import settings
from django.shortcuts import redirect
from .models import Seller

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
            return redirect('sellers:product_list')
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
@login_required
def product_list_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    
    context = {
        'products': products,
        'seller': seller
    }
    return render(request, 'seller/product_list.html', context)


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
        return redirect('sellers:product_list')
    
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
    """Main seller dashboard with overview stats and recent data"""
    seller = get_object_or_404(Seller, user=request.user)
    
    # Get orders for this seller
    orders = Order.objects.filter(seller=seller).order_by('-created_at')
    
    # Calculate dashboard stats
    total_earnings = sum(order.total_amount for order in orders if order.payment_status == 'paid')
    total_orders = orders.count()
    total_products = Product.objects.filter(seller=seller).count()
    
    # Monthly sales (current month)
    from django.utils import timezone
    from datetime import datetime
    current_month = timezone.now().month
    monthly_sales = sum(order.total_amount for order in orders 
                       if order.payment_status == 'paid' and order.created_at.month == current_month)
    
    # Recent orders (last 10)
    recent_orders = orders[:10]
    
    # Get seller's products
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    
    # Calculate revenue breakdown
    weekly_revenue = sum(order.total_amount for order in orders 
                        if order.payment_status == 'paid' and 
                        order.created_at >= timezone.now() - timezone.timedelta(days=7))
    
    yearly_revenue = sum(order.total_amount for order in orders 
                        if order.payment_status == 'paid' and 
                        order.created_at.year == timezone.now().year)
    
    # Top selling products (simplified - in real app you'd track sales)
    top_products = products[:5]  # Just show recent products for now
    
    # Mock notifications (in real app these would come from a notification system)
    notifications = [
        {
            'type': 'order',
            'title': 'New Order Received',
            'message': 'Order #1234 has been placed',
            'created_at': timezone.now() - timezone.timedelta(hours=2)
        },
        {
            'type': 'stock',
            'title': 'Low Stock Alert',
            'message': 'Product "Premium T-Shirt" is running low',
            'created_at': timezone.now() - timezone.timedelta(days=1)
        }
    ]
    
    # Get categories for product form
    categories = Category.objects.all()
    
    context = {
        'seller': seller,
        'total_earnings': total_earnings,
        'total_orders': total_orders,
        'total_products': total_products,
        'monthly_sales': monthly_sales,
        'recent_orders': recent_orders,
        'products': products,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_sales,
        'yearly_revenue': yearly_revenue,
        'top_products': top_products,
        'notifications': notifications,
        'categories': categories,
    }
    return render(request, 'seller/seller_dashboard.html', context)

@login_required
def seller_orders_list(request):
    """Detailed orders list for seller"""
    seller = get_object_or_404(Seller, user=request.user)
    orders = Order.objects.filter(seller=seller).order_by('-created_at')
    
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
    return render(request, 'seller/add_product.html', context)

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
    return render(request, 'seller/delete_product.html', context)

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
    
    # Top selling products (simplified)
    top_products = Product.objects.filter(seller=seller)[:5]
    
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
