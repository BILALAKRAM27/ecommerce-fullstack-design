from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Buyer, Cart, CartItem, Wishlist
from .forms import BuyerUpdateForm
from seller.models import Product
from .utils import get_cart_from_cookie, set_cart_cookie, clear_cart_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.
@login_required
def buyer_profile_view(request):
    try:
        buyer = Buyer.objects.get(email=request.user.email)
        context = {
            'buyer': buyer,
            'image_base64': buyer.get_image_base64()
        }
        return render(request, 'buyer/buyer_profile.html', context)
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer profile not found.')
        return redirect('sellers:login')


# UPDATE Buyer
@login_required
def update_buyer_view(request):
    try:
        buyer = Buyer.objects.get(email=request.user.email)
        if request.method == 'POST':
            form = BuyerUpdateForm(request.POST, request.FILES, instance=buyer)
            if form.is_valid():
                buyer = form.save()
                messages.success(request, 'Buyer profile updated successfully.')
                return redirect('buyer:buyer_profile')
        else:
            form = BuyerUpdateForm(instance=buyer)
        return render(request, 'buyer/buyer_update.html', {'form': form})
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer profile not found.')
        return redirect('sellers:login')


# DELETE Buyer
@login_required
def delete_buyer_view(request):
    try:
        buyer = Buyer.objects.get(email=request.user.email)
        if request.method == 'POST':
            # Delete the buyer profile
            buyer.delete()
            messages.success(request, 'Your buyer account has been deleted.')
            return redirect('sellers:login')
        return render(request, 'buyer/buyer_delete.html')
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer profile not found.')
        return redirect('sellers:login')


def get_cart(request):
    if request.user.is_authenticated:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        items = [
            {
                "product_id": item.product.id,
                "name": item.product.name,
                "price": item.product.final_price,
                "quantity": item.quantity,
                "total_price": item.get_total_price()
            }
            for item in cart.items.select_related('product')
        ]
        subtotal = sum(item["total_price"] for item in items)
        discount = 0
        tax = 0
        total = subtotal
        return {
            "items": items,
            "is_authenticated": True,
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "total": total
        }
    else:
        cart_data = get_cart_from_cookie(request)
        # Calculate subtotal, discount, tax, total for guest cart
        items = []
        subtotal = 0
        for entry in cart_data.get('items', []):
            try:
                product = Product.objects.get(id=entry['product_id'])
                total_price = product.final_price * entry['quantity']
                items.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.final_price,
                    "quantity": entry['quantity'],
                    "total_price": total_price
                })
                subtotal += total_price
            except Product.DoesNotExist:
                continue
        discount = 0
        tax = 0
        total = subtotal
        cart_data.update({
            "items": items,
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "total": total
        })
        return cart_data

def add_to_cart(request):
    product_id = int(request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        cart.add_product(product, quantity)
        # Return a success response
        return JsonResponse({'success': True})
    else:
        cart_data = get_cart_from_cookie(request)
        for item in cart_data["items"]:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            cart_data["items"].append({"product_id": product_id, "quantity": quantity})
        response = JsonResponse({"success": True, "cart": cart_data})
        set_cart_cookie(response, cart_data)
        return response

def remove_from_cart(request):
    product_id = int(request.POST.get('product_id'))
    if request.user.is_authenticated:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        product = get_object_or_404(Product, id=product_id)
        cart.remove_product(product)
        cart_data = get_cart(request)
        if isinstance(cart_data, JsonResponse):
            import json
            cart_data = json.loads(cart_data.content)
        return JsonResponse({"success": True, "cart": cart_data})
    else:
        cart_data = get_cart_from_cookie(request)
        new_items = [item for item in cart_data["items"] if item["product_id"] != product_id]
        cart_data["items"] = new_items
        response = JsonResponse({"success": True, "cart": cart_data})
        set_cart_cookie(response, cart_data)
        return response

@require_POST
def update_cart_quantity(request):
    try:
        print("=== Starting cart quantity update ===")
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        print(f"Received request - Product ID: {product_id}, Quantity: {quantity}")
        
        # Get the product first to validate it exists
        try:
            product = Product.objects.get(id=product_id)
            print(f"Found product: {product.name}, Price: {product.final_price:.2f}")
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Product not found'
            })

        if request.user.is_authenticated:
            try:
                buyer = Buyer.objects.get(email=request.user.email)
                cart, _ = Cart.objects.get_or_create(buyer=buyer)
                
                if quantity > 0:
                    cart_item = cart.update_quantity(product, quantity)
                else:
                    cart.remove_product(product)
                
                # Get updated cart data
                cart_data = cart.get_cart_data()
                print(f"Cart data after update: {cart_data}")
                return JsonResponse(cart_data)
                
            except Buyer.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Buyer not found'
                })
            except Exception as e:
                print(f"Error updating cart: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': f'Error updating cart: {str(e)}'
                })
        else:
            # Handle guest cart in session
            cart_data = request.session.get('cart', {'items': [], 'coupon_code': None})
            
            # Update or remove item
            updated_items = []
            subtotal = 0
            cart_count = 0
            
            for item in cart_data['items']:
                if item['product_id'] == product_id:
                    if quantity > 0:
                        item['quantity'] = quantity
                        updated_items.append(item)
                else:
                    updated_items.append(item)
                    
            cart_data['items'] = updated_items
            
            # Calculate totals
            for item in cart_data['items']:
                try:
                    prod = Product.objects.get(id=item['product_id'])
                    subtotal += round(prod.final_price * item['quantity'], 2)
                    cart_count += item['quantity']
                except Product.DoesNotExist:
                    continue
            
            # Apply discount
            discount_percentage = 0.20 if cart_data.get('coupon_code') in ["MarketVibe27", "Shopping24/7"] else 0.10
            discount = round(subtotal * discount_percentage, 2)
            tax = round((subtotal - discount) * 0.10, 2)
            total = round(subtotal - discount + tax, 2)
            
            # Update session
            request.session['cart'] = cart_data
            request.session.modified = True
            
            response_data = {
                'success': True,
                'cart_count': cart_count,
                'subtotal': float(subtotal),
                'discount_percentage': discount_percentage * 100,
                'discount': float(discount),
                'tax': float(tax),
                'total': float(total),
                'coupon_code': cart_data.get('coupon_code')
            }
            
            return JsonResponse(response_data)
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_POST
def apply_coupon(request):
    try:
        code = request.POST.get('code')
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'No coupon code provided'
            })
            
        if request.user.is_authenticated:
            buyer = Buyer.objects.get(email=request.user.email)
            cart, _ = Cart.objects.get_or_create(buyer=buyer)
            
            if cart.apply_coupon(code):
                return JsonResponse(cart.get_cart_data())
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid coupon code'
                })
        else:
            # Handle guest cart
            cart_data = request.session.get('cart', {'items': [], 'coupon_code': None})
            
            if code in ["MarketVibe27", "Shopping24/7"]:
                cart_data['coupon_code'] = code
                request.session['cart'] = cart_data
                request.session.modified = True
                
                # Recalculate totals
                subtotal = 0
                cart_count = 0
                
                for item in cart_data['items']:
                    try:
                        prod = Product.objects.get(id=item['product_id'])
                        subtotal += round(prod.final_price * item['quantity'], 2)
                        cart_count += item['quantity']
                    except Product.DoesNotExist:
                        continue
                
                discount = round(subtotal * 0.20, 2)  # 20% discount for valid coupon
                tax = round((subtotal - discount) * 0.10, 2)
                total = round(subtotal - discount + tax, 2)
                
                return JsonResponse({
                    'success': True,
                    'cart_count': cart_count,
                    'subtotal': float(subtotal),
                    'discount_percentage': 20.0,
                    'discount': float(discount),
                    'tax': float(tax),
                    'total': float(total),
                    'coupon_code': code
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid coupon code'
                })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def clear_cart(request):
    if request.user.is_authenticated:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        cart.clear()
        return get_cart(request)
    else:
        response = JsonResponse({"success": True, "cart": {"items": []}})
        clear_cart_cookie(response)
        return response

@require_POST
def add_to_wishlist(request):
    print("=== Adding to wishlist ===")
    try:
        product_id = int(request.POST.get('product_id'))
        print(f"Product ID: {product_id}")
        
        if not request.user.is_authenticated:
            print("User not authenticated")
            return JsonResponse({
                'success': False,
                'error': 'Please login to save items'
            })
        
        try:
            product = Product.objects.get(id=product_id)
            print(f"Found product: {product.name}")
        except Product.DoesNotExist:
            print(f"Product not found with ID: {product_id}")
            return JsonResponse({
                'success': False,
                'error': 'Product not found'
            })
        
        buyer = get_object_or_404(Buyer, email=request.user.email)
        print(f"Found buyer: {buyer.name}")
        
        # Check if already in cart
        cart = Cart.objects.filter(buyer=buyer).first()
        if cart and cart.items.filter(product=product).exists():
            return JsonResponse({
                'success': False,
                'error': 'This item is already in your cart.'
            })
        
        # Check if already in wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(
            buyer=buyer,
            product=product
        )
        print(f"Wishlist item {'created' if created else 'already exists'}")
        
        return JsonResponse({
            'success': True,
            'message': 'Added to wishlist'
        })
        
    except Exception as e:
        print(f"Error adding to wishlist: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_POST
def remove_from_wishlist(request):
    print("=== Removing from wishlist ===")
    try:
        product_id = int(request.POST.get('product_id'))
        print(f"Product ID: {product_id}")
        
        if not request.user.is_authenticated:
            print("User not authenticated")
            return JsonResponse({
                'success': False,
                'error': 'Please login to manage wishlist'
            })
            
        buyer = get_object_or_404(Buyer, email=request.user.email)
        print(f"Found buyer: {buyer.name}")
        
        result = Wishlist.objects.filter(buyer=buyer, product_id=product_id).delete()
        print(f"Delete result: {result}")
        
        return JsonResponse({
            'success': True,
            'message': 'Removed from wishlist'
        })
        
    except Exception as e:
        print(f"Error removing from wishlist: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@require_POST
def remove_all_from_cart(request):
    try:
        if request.user.is_authenticated:
            buyer = get_object_or_404(Buyer, email=request.user.email)
            cart, _ = Cart.objects.get_or_create(buyer=buyer)
            cart.clear()  # Using the existing clear method from Cart model
            
            return JsonResponse({
                'success': True,
                'message': 'All items removed from cart',
                'cart_count': 0,
                'subtotal': 0,
                'tax': 0,
                'discount': 0,
                'total': 0
            })
        else:
            # Handle guest cart
            request.session['cart'] = {'items': []}
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': 'All items removed from cart',
                'cart_count': 0,
                'subtotal': 0,
                'tax': 0,
                'discount': 0,
                'total': 0
            })
            
    except Exception as e:
        print(f"Error removing all items from cart: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# Update the cart_page_view to include wishlist items
def cart_page_view(request):
    if request.user.is_authenticated:
        buyer = Buyer.objects.get(email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        items = cart.items.select_related('product')
        cart_items = [{
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item.get_total_price()
        } for item in items]
        
        # Get wishlist items
        wishlist_items = Wishlist.objects.filter(buyer=buyer).select_related('product')
        
        subtotal = cart.subtotal
        discount = cart.discount_amount
        tax = cart.tax
        total = cart.total
        discount_percentage = cart.get_discount_percentage() * 100
    else:
        cart_data = request.session.get('cart', {'items': []})
        cart_items = []
        wishlist_items = []  # Empty list for non-authenticated users
        subtotal = 0
        
        for entry in cart_data['items']:
            try:
                product = Product.objects.get(id=entry['product_id'])
                item_total = product.final_price * entry['quantity']
                cart_items.append({
                    'product': product,
                    'quantity': entry['quantity'],
                    'total_price': item_total
                })
                subtotal += item_total
            except Product.DoesNotExist:
                continue
                
        discount_percentage = 0.20 if cart_data.get('coupon_code') in ["MarketVibe27", "Shopping24/7"] else 0.10
        discount = round(subtotal * discount_percentage, 2)
        tax = round((subtotal - discount) * 0.10, 2)
        total = round(subtotal - discount + tax, 2)
        discount_percentage *= 100

    context = {
        'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'total': total,
        'discount_percentage': discount_percentage
    }
    return render(request, 'buyer/cart_page.html', context)