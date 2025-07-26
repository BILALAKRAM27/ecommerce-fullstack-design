from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Buyer, Cart, CartItem, Wishlist, Address
from .forms import BuyerUpdateForm
from seller.models import Product
from .utils import get_cart_from_cookie, set_cart_cookie, clear_cart_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils_order import group_cart_items_by_seller, calculate_order_summary, generate_order_id
from .models import Order, OrderItem
import base64
import stripe
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Payment


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

@login_required(login_url='/seller/login/')
def add_to_cart(request):
    product_id = int(request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        cart.add_product(product, quantity)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            # Redirect to cart page after adding
            return redirect('buyer:cart_page')  # Make sure this is the correct name for your cart page view
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

@login_required
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

@login_required
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
@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def checkout_view(request):
    buyer = get_object_or_404(Buyer, email=request.user.email)
    cart, _ = Cart.objects.get_or_create(buyer=buyer)
    cart_items = cart.items.select_related('product__seller')

    grouped_sellers = []
    seller_map = {}
    for item in cart_items:
        seller = item.product.seller
        if seller.id not in seller_map:
            seller_map[seller.id] = {
                'seller': {'shop_name': seller.shop_name},
                'products': [],
                'subtotal': 0,
            }
        img_obj = item.product.images.first()
        if img_obj and img_obj.image:
            image_url = f"data:image/jpeg;base64,{base64.b64encode(img_obj.image).decode()}"
        else:
            image_url = ""
        seller_map[seller.id]['products'].append({
            'name': item.product.name,
            'image_url': image_url,
            'attributes': ', '.join([f"{av.attribute.name}: {av.value}" for av in item.product.attribute_values.all()]),
            'quantity': item.quantity,
            'price': item.product.final_price,
        })
        seller_map[seller.id]['subtotal'] += item.product.final_price * item.quantity
    grouped_sellers = list(seller_map.values())

    subtotal = cart.subtotal
    shipping = 15.99  # Example fixed shipping
    tax = round((subtotal - cart.discount_amount) * 0.10, 2)
    total = round(subtotal - cart.discount_amount + tax + shipping, 2)
    total_items = sum(item.quantity for item in cart_items)
    order_summary = {
        'subtotal': subtotal, 'shipping': shipping, 'tax': tax, 'total': total, 'total_items': total_items,
    }

    address_obj = getattr(buyer, 'address', None)
    shipping_address = {
        'street': address_obj.street if address_obj else '', 'city': address_obj.city if address_obj else '',
        'zip_code': address_obj.zip_code if address_obj else '', 'country': address_obj.country if address_obj else 'US',
    }

    context = {
        'grouped_sellers': grouped_sellers, 'order_summary': order_summary,
        'shipping_address': shipping_address, 'buyer': buyer,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'buyer/checkout_page.html', context)

@login_required
def order_summary_view(request):
    buyer = get_object_or_404(Buyer, email=request.user.email)
    cart, _ = Cart.objects.get_or_create(buyer=buyer)
    items = cart.items.select_related('product__seller')

    # Group items by seller
    sellers = {}
    for item in items:
        seller = item.product.seller
        if seller.id not in sellers:
            sellers[seller.id] = {
                'seller': seller,
                'products': []
            }
        sellers[seller.id]['products'].append(item)

    context = {
        'sellers': sellers.values()
    }
    return render(request, 'buyer/checkout_page.html', context)

@login_required
@require_POST
def place_order_view(request):
    """Handle COD order placement"""
    try:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        cart_items = cart.items.select_related('product__seller')
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'})
        
        # Get shipping address from request
        import json
        data = json.loads(request.body)
        shipping_address = data.get('shipping_address', {})
        shipping_address_str = f"{shipping_address.get('street', '')}, {shipping_address.get('city', '')}, {shipping_address.get('zip_code', '')}, {shipping_address.get('country', '')}"
        
        # Create orders for each seller
        orders_created = []
        
        for item in cart_items:
            seller = item.product.seller
            
            # Create order
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                status='pending',
                total_amount=item.get_total_price(),
                payment_status='pending',
                order_type='cod',
                delivery_address=shipping_address_str,
            )
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price_at_purchase=item.product.final_price,
                quantity=item.quantity,
            )
            
            # Increment product order count and decrement stock
            item.product.order_count += 1
            item.product.stock -= item.quantity
            item.product.save()
            
            orders_created.append(order)
        
        # Clear cart after creating orders
        cart.clear()
        
        return JsonResponse({
            'success': True,
            'orders': [order.id for order in orders_created]
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_payment_intent(order, seller):
    # Calculate amounts
    amount = int(order.total_amount * 100)  # in cents
    commission = int(order.total_amount * 0.10 * 100)  # 10% commission, in cents

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        payment_method_types=["card"],
        application_fee_amount=commission,
        transfer_data={
            "destination": seller.stripe_account_id,
        },
        metadata={
            "order_id": order.id,
        }
    )
    return payment_intent.client_secret

@login_required
@require_POST
def process_stripe_payment(request):
    """Handle Stripe payment processing during checkout"""
    try:
        buyer = get_object_or_404(Buyer, email=request.user.email)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        cart_items = cart.items.select_related('product__seller')
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'})
        
        # Get shipping address from form
        shipping_address = request.POST.get('shipping_address', '')
        
        # Group items by seller and check Stripe setup
        seller_groups = {}
        stripe_ready_sellers = []
        non_stripe_sellers = []
        
        for item in cart_items:
            seller = item.product.seller
            if seller.id not in seller_groups:
                seller_groups[seller.id] = {
                    'seller': seller,
                    'items': [],
                    'total': 0
                }
            
            seller_groups[seller.id]['items'].append(item)
            seller_groups[seller.id]['total'] += item.get_total_price()
            
            # Check if seller has Stripe account
            if seller.stripe_account_id:
                stripe_ready_sellers.append(seller.id)
            else:
                non_stripe_sellers.append(seller.shop_name)
        
        # If any seller doesn't have Stripe, provide options
        if non_stripe_sellers:
            return JsonResponse({
                'success': False,
                'error': 'Some sellers are not set up for online payments',
                'non_stripe_sellers': non_stripe_sellers,
                'stripe_ready_sellers': stripe_ready_sellers,
                'suggestion': 'Please contact these sellers to set up payments or choose Cash on Delivery'
            })
        
        # All sellers have Stripe - proceed with payment
        payment_intents = []
        orders_created = []
        
        for seller_id, group in seller_groups.items():
            seller = group['seller']
            
            # Calculate shipping per seller
            shipping_per_seller = 15.99 / len(seller_groups)

            # Create order
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                status='pending',
                total_amount=group['total'] + shipping_per_seller,  # Add shipping here
                payment_status='pending',
                order_type='stripe',
                delivery_address=shipping_address,
            )
            
            # Create order items
            for item in group['items']:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price_at_purchase=item.product.final_price,
                    quantity=item.quantity,
                )
                
                # Increment product order count and decrement stock
                item.product.order_count += 1
                item.product.stock -= item.quantity
                item.product.save()
            
            # Create Stripe PaymentIntent
            client_secret = create_stripe_payment_intent(order, seller)
            payment_intents.append({
                'order_id': order.id,
                'client_secret': client_secret,
                'amount': order.total_amount
            })
            orders_created.append(order)
        
        # Clear cart after creating orders
        cart.clear()
        
        return JsonResponse({
            'success': True,
            'payment_intents': payment_intents,
            'orders': [order.id for order in orders_created]
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
def stripe_webhook(request):
    import stripe
    from django.conf import settings
    from .models import Payment

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # For local development, if signature is missing, try to process without verification
    if not sig_header and settings.DEBUG:
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
    else:
        if not sig_header:
            return HttpResponse(status=400)
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent['metadata'].get('order_id')
        
        if not order_id:
            print(f"DEBUG: No order_id found in metadata: {intent['metadata']}")
            return HttpResponse(status=400)
        
        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                payment_method='stripe',
                transaction_id=intent.id,
                status='paid',
                payment_time=timezone.now()
            )
            print(f"DEBUG: Payment record created: {payment.id} for order {order_id}")
            
        except Order.DoesNotExist:
            print(f"DEBUG: Order {order_id} not found")
            return HttpResponse(status=404)
        except Exception as e:
            print(f"DEBUG: Error creating payment: {str(e)}")
            return HttpResponse(status=500)

    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        order_id = intent['metadata']['order_id']
        
        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = 'failed'
            order.save()
            
            # Create payment record
            Payment.objects.create(
                order=order,
                payment_method='stripe',
                transaction_id=intent.id,
                status='failed',
                payment_time=timezone.now()
            )
            
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)

@login_required
@require_POST
def fetch_order_details(request):
    """Fetch order details for receipt display"""
    print(f"DEBUG: fetch_order_details called with body: {request.body}")
    try:
        data = json.loads(request.body)
        order_ids = data.get('order_ids', [])
        print(f"DEBUG: Order IDs received: {order_ids}")
        
        if not order_ids:
            print("DEBUG: No order IDs provided")
            return JsonResponse({
                'success': False,
                'error': 'No order IDs provided'
            })
        
        grouped_order_details = []
        
        for order_id in order_ids:
            try:
                order = Order.objects.get(id=order_id)
                order_items = OrderItem.objects.filter(order=order).select_related('product')
                
                # Group items by seller
                seller_items = {}
                for item in order_items:
                    seller = item.product.seller
                    if seller.id not in seller_items:
                        seller_items[seller.id] = {
                            'seller_name': seller.shop_name,
                            'items': [],
                            'subtotal': 0
                        }
                    
                    seller_items[seller.id]['items'].append({
                        'name': item.product.name,
                        'quantity': item.quantity,
                        'price': item.price_at_purchase
                    })
                    seller_items[seller.id]['subtotal'] += item.price_at_purchase * item.quantity
                
                # Add order payment status - check if there's a successful payment record
                payment_status = order.payment_status
                # Check if there's a successful payment record for this order
                try:
                    payment = Payment.objects.get(order=order, status='paid')
                    payment_status = 'paid'
                except Payment.DoesNotExist:
                    # If no successful payment found, use the order's payment_status
                    pass
                
                # Convert to list format
                for seller_data in seller_items.values():
                    grouped_order_details.append(seller_data)
                    
            except Order.DoesNotExist:
                continue
        
        print(f"DEBUG: Returning grouped order details: {grouped_order_details}")
        return JsonResponse({
            'success': True,
            'grouped_order_details': grouped_order_details,
            'payment_status': payment_status if 'payment_status' in locals() else 'unknown'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })