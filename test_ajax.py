#!/usr/bin/env python
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from django.test import RequestFactory
from seller.views import get_category_attributes
from seller.models import Category

def test_ajax_endpoint():
    print("=== Testing AJAX Endpoint ===")
    
    # Create a test request
    factory = RequestFactory()
    
    # Test with Clothing category
    clothing = Category.objects.filter(name='Clothing').first()
    if clothing:
        print(f"Testing with Clothing category (ID: {clothing.id})")
        
        # Create the request
        request = factory.post('/ajax/get-category-attributes/', 
                             data=json.dumps({'category_id': clothing.id}),
                             content_type='application/json')
        
        # Call the view
        response = get_category_attributes(request)
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        # Parse the response
        try:
            data = json.loads(response.content.decode())
            print(f"\nParsed data:")
            print(f"Number of attributes: {len(data.get('attributes', []))}")
            for attr in data.get('attributes', []):
                print(f"- {attr['name']} ({attr['input_type']}): {len(attr['options'])} options")
                for opt in attr['options']:
                    print(f"  * {opt['value']}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    
    # Test with Electronics category
    electronics = Category.objects.filter(name='Electronics').first()
    if electronics:
        print(f"\nTesting with Electronics category (ID: {electronics.id})")
        
        request = factory.post('/ajax/get-category-attributes/', 
                             data=json.dumps({'category_id': electronics.id}),
                             content_type='application/json')
        
        response = get_category_attributes(request)
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")

if __name__ == "__main__":
    test_ajax_endpoint() 