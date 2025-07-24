import uuid

def group_cart_items_by_seller(cart_items):
    sellers = {}
    for item in cart_items:
        seller = item.product.seller
        if seller.id not in sellers:
            sellers[seller.id] = {
                'seller': seller,
                'products': []
            }
        sellers[seller.id]['products'].append(item)
    return list(sellers.values())

def calculate_order_summary(cart):
    subtotal = cart.subtotal
    discount = cart.discount_amount
    tax = cart.tax
    shipping = cart.shipping_cost if hasattr(cart, 'shipping_cost') else 0
    total = cart.total + shipping
    return {
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'shipping': shipping,
        'total': total
    }

def generate_order_id():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]
