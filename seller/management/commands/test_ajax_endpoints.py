#!/usr/bin/env python3
"""
Test script to verify AJAX endpoints are working
"""
import requests
import json

# Base URL for the Django server
BASE_URL = "http://localhost:8000"

def test_category_children():
    """Test the get_category_children endpoint"""
    print("Testing get_category_children endpoint...")
    
    # Test data
    data = {
        "parent_id": 1  # Assuming category ID 1 exists
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ajax/get-category-children/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                print(f"Children found: {len(result.get('children', []))}")
        
    except Exception as e:
        print(f"Error testing category children: {e}")

def test_category_attributes():
    """Test the get_category_attributes endpoint"""
    print("\nTesting get_category_attributes endpoint...")
    
    # Test data
    data = {
        "category_id": 1  # Assuming category ID 1 exists
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ajax/get-category-attributes/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                print(f"Attributes found: {len(result.get('attributes', []))}")
        
    except Exception as e:
        print(f"Error testing category attributes: {e}")

def test_filtered_products():
    """Test the get_filtered_products endpoint"""
    print("\nTesting get_filtered_products endpoint...")
    
    # Test parameters
    params = {
        "parent_category": 1,
        "min_price": 0,
        "max_price": 1000
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/ajax/get-filtered-products/",
            params=params
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # Show first 500 chars
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                print(f"Products found: {len(result.get('products', []))}")
        
    except Exception as e:
        print(f"Error testing filtered products: {e}")

if __name__ == "__main__":
    print("Testing AJAX endpoints...")
    test_category_children()
    test_category_attributes()
    test_filtered_products()
    print("\nTesting complete!") 