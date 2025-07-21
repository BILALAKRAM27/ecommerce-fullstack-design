import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Seller, Product, ProductImage, Brand, Category, CategoryAttribute, AttributeOption
from .forms import UserRegisterForm, SellerUpdateForm, SellerLoginForm, ProductForm, ProductImageForm, DynamicProductForm
from django.utils import timezone
from buyer.models import Buyer 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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
    seller = get_object_or_404(Seller, user=request.user) if request.user.is_authenticated else None
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'seller': seller,
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
            messages.success(request, 'Product updated successfully!')
            return redirect('sellers:product_detail', product_id=product.id)
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
