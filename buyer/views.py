from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Buyer, Cart, CartItem
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
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity
        if quantity < 1:
            return JsonResponse({
                'success': False,
                'error': 'Quantity must be at least 1'
            })

        # Get or create cart based on user authentication status
        if request.user.is_authenticated:
            buyer = get_object_or_404(Buyer, email=request.user.email)
            cart, _ = Cart.objects.get_or_create(buyer=buyer)
            
            try:
                product = Product.objects.get(id=product_id)
                
                # Update quantity in cart
                cart.update_quantity(product, quantity)
                
                # Get updated cart data
                cart_items = cart.items.all()
                subtotal = sum(item.get_total_price() for item in cart_items)
                cart_count = cart.total_items
                
                return JsonResponse({
                    'success': True,
                    'cart_count': cart_count,
                    'subtotal': subtotal,
                    'message': 'Cart updated successfully'
                })
                
            except Product.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Product not found'
                })
                
        else:
            # Handle guest cart in session/cookies
            cart_data = request.session.get('cart', {'items': []})
            
            # Find and update item quantity
            found = False
            for item in cart_data['items']:
                if item['product_id'] == product_id:
                    item['quantity'] = quantity
                    found = True
                    break
                    
            if not found:
                return JsonResponse({
                    'success': False,
                    'error': 'Product not found in cart'
                })
                
            # Update session
            request.session['cart'] = cart_data
            request.session.modified = True
            
            # Calculate totals
            cart_count = sum(item['quantity'] for item in cart_data['items'])
            
            return JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'message': 'Cart updated successfully'
            })
            
    except (ValueError, TypeError) as e:
        return JsonResponse({
            'success': False,
            'error': 'Invalid quantity or product ID'
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
    else:
        cart_data = get_cart_from_cookie(request)
        cart_items = []
        for entry in cart_data['items']:
            try:
                product = Product.objects.get(id=entry['product_id'])
                cart_items.append({
                    'product': product,
                    'quantity': entry['quantity'],
                    'total_price': product.final_price * entry['quantity']
                })
            except Product.DoesNotExist:
                continue
    subtotal = sum(item['total_price'] for item in cart_items)
    # You can add logic for discount, tax, etc.
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': 0,
        'tax': 0,
        'total': subtotal,
    }
    return render(request, 'buyer/cart_page.html', context)