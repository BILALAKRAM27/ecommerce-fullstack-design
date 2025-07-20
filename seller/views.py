import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Seller
from .forms import UserRegisterForm, SellerUpdateForm, SellerLoginForm
from django.utils import timezone
from buyer.models import Buyer 


def index_view(request):
    return render(request, "index.html")

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
