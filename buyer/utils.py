import json

CART_COOKIE_NAME = 'cart'
CART_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week

def get_cart_from_cookie(request):
    cart_json = request.COOKIES.get(CART_COOKIE_NAME)
    if cart_json:
        try:
            return json.loads(cart_json)
        except Exception:
            return {"items": []}
    return {"items": []}

def set_cart_cookie(response, cart_data):
    response.set_cookie(CART_COOKIE_NAME, json.dumps(cart_data), max_age=CART_COOKIE_AGE, httponly=False)

def clear_cart_cookie(response):
    response.delete_cookie(CART_COOKIE_NAME) 