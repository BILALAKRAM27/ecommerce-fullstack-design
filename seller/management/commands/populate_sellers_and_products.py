#!/usr/bin/env python
"""
Script to populate MarketVibe database with 20 seller accounts and 100 products
Run this script from the Django project root directory
"""

import os
import sys
import django
import random
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from django.contrib.auth.models import User
from seller.models import Seller, Product, Category, Brand, ProductCondition
from seller.models import ProductImage

def create_user_and_seller(seller_number):
    """Create a user and seller account"""
    email = f"seller{seller_number}@gmail.com"
    username = f"seller{seller_number}"
    
    # Create user
    user, user_created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': f'Seller{seller_number}',
            'last_name': 'User',
            'is_active': True
        }
    )
    
    if user_created:
        user.set_password("marketvibe27")
        user.save()
        print(f"✓ Created user: {username}")
    
    # Create seller
    shop_names = [
        "Tech Haven", "Digital Dreams", "Smart Solutions", "Gadget Galaxy", "Tech Trends",
        "Digital Depot", "Smart Store", "Tech Tower", "Gadget Garden", "Digital Domain",
        "Smart Spot", "Tech Terrace", "Gadget Grove", "Digital Den", "Smart Space",
        "Tech Town", "Gadget Garage", "Digital Drive", "Smart Station", "Tech Terrace"
    ]
    
    shop_descriptions = [
        "Your one-stop shop for all things tech and electronics",
        "Premium gadgets and electronics for the modern lifestyle",
        "Quality electronics and smart devices at competitive prices",
        "Innovative tech solutions for every need",
        "Reliable electronics and gadgets for everyone",
        "Expert tech solutions and premium electronics",
        "Your trusted source for quality electronics",
        "Modern gadgets and tech accessories",
        "Professional electronics and smart devices",
        "Quality tech products for every budget",
        "Innovative electronics and smart solutions",
        "Your tech partner for all digital needs",
        "Premium electronics and gadget solutions",
        "Reliable tech products and accessories",
        "Smart devices and electronics for everyone",
        "Quality electronics and tech solutions",
        "Your digital lifestyle partner",
        "Innovative tech products and services",
        "Premium electronics and smart gadgets",
        "Your trusted tech destination"
    ]
    
    seller, seller_created = Seller.objects.get_or_create(
        email=email,
        defaults={
            'user': user,
            'name': f'Seller{seller_number}',
            'shop_name': shop_names[seller_number - 1],
            'shop_description': shop_descriptions[seller_number - 1],
            'address': f'Shop {seller_number}, Tech Street, Digital City, DC {10000 + seller_number}',
            'rating': round(random.uniform(3.5, 5.0), 1)
        }
    )
    
    if seller_created:
        print(f"✓ Created seller: {seller.shop_name}")
    
    return seller

def get_random_category_and_brand():
    """Get a random subcategory and its associated brand"""
    # Get all subcategories (categories with parents)
    subcategories = Category.objects.filter(parent__isnull=False)
    
    if not subcategories.exists():
        raise Exception("No subcategories found. Please run category population scripts first.")
    
    # Select a random subcategory
    category = random.choice(subcategories)
    
    # Get brands for this category (we'll use any available brand)
    brands = Brand.objects.all()
    
    if not brands.exists():
        raise Exception("No brands found. Please run brand population script first.")
    
    brand = random.choice(brands)
    
    return category, brand

def generate_product_data(category, brand, product_number):
    """Generate product data based on category"""
    
    # Product templates for different categories
    product_templates = {
        # Electronics
        "Smartphones": [
            {"name": "Premium Smartphone", "base_price": 599.99, "stock": 50},
            {"name": "Flagship Mobile", "base_price": 899.99, "stock": 30},
            {"name": "Budget Smartphone", "base_price": 299.99, "stock": 100},
            {"name": "5G Smartphone", "base_price": 699.99, "stock": 40},
            {"name": "Camera Phone", "base_price": 799.99, "stock": 35}
        ],
        "Laptops": [
            {"name": "Gaming Laptop", "base_price": 1299.99, "stock": 25},
            {"name": "Business Laptop", "base_price": 899.99, "stock": 40},
            {"name": "Student Laptop", "base_price": 599.99, "stock": 60},
            {"name": "Ultrabook", "base_price": 1099.99, "stock": 30},
            {"name": "Workstation Laptop", "base_price": 1499.99, "stock": 20}
        ],
        "Smart Watches": [
            {"name": "Fitness Smartwatch", "base_price": 199.99, "stock": 80},
            {"name": "Premium Smartwatch", "base_price": 399.99, "stock": 45},
            {"name": "Sports Watch", "base_price": 299.99, "stock": 60},
            {"name": "Health Monitor", "base_price": 249.99, "stock": 70},
            {"name": "Luxury Smartwatch", "base_price": 599.99, "stock": 25}
        ],
        "LED TVs": [
            {"name": "4K Smart TV", "base_price": 799.99, "stock": 35},
            {"name": "Gaming TV", "base_price": 899.99, "stock": 30},
            {"name": "Home Theater TV", "base_price": 1299.99, "stock": 20},
            {"name": "Budget TV", "base_price": 399.99, "stock": 50},
            {"name": "Premium OLED TV", "base_price": 1999.99, "stock": 15}
        ],
        "Bluetooth Speakers": [
            {"name": "Portable Speaker", "base_price": 89.99, "stock": 100},
            {"name": "Waterproof Speaker", "base_price": 129.99, "stock": 75},
            {"name": "Party Speaker", "base_price": 199.99, "stock": 50},
            {"name": "Mini Speaker", "base_price": 49.99, "stock": 150},
            {"name": "Premium Speaker", "base_price": 299.99, "stock": 40}
        ],
        "Cameras": [
            {"name": "DSLR Camera", "base_price": 899.99, "stock": 30},
            {"name": "Mirrorless Camera", "base_price": 1099.99, "stock": 25},
            {"name": "Action Camera", "base_price": 299.99, "stock": 80},
            {"name": "Point & Shoot", "base_price": 199.99, "stock": 60},
            {"name": "Professional Camera", "base_price": 2499.99, "stock": 10}
        ],
        "Headphones": [
            {"name": "Wireless Headphones", "base_price": 199.99, "stock": 70},
            {"name": "Noise Cancelling", "base_price": 299.99, "stock": 50},
            {"name": "Gaming Headset", "base_price": 149.99, "stock": 80},
            {"name": "Studio Headphones", "base_price": 399.99, "stock": 40},
            {"name": "Sports Headphones", "base_price": 89.99, "stock": 100}
        ],
        "Power Banks": [
            {"name": "High Capacity Power Bank", "base_price": 79.99, "stock": 120},
            {"name": "Fast Charging Power Bank", "base_price": 99.99, "stock": 90},
            {"name": "Compact Power Bank", "base_price": 49.99, "stock": 150},
            {"name": "Wireless Power Bank", "base_price": 129.99, "stock": 70},
            {"name": "Solar Power Bank", "base_price": 149.99, "stock": 60}
        ],
        "Gaming Consoles": [
            {"name": "Gaming Console", "base_price": 499.99, "stock": 40},
            {"name": "Handheld Console", "base_price": 299.99, "stock": 60},
            {"name": "Retro Console", "base_price": 199.99, "stock": 80},
            {"name": "VR Gaming Set", "base_price": 399.99, "stock": 30},
            {"name": "Gaming Bundle", "base_price": 699.99, "stock": 25}
        ],
        "Drones": [
            {"name": "Camera Drone", "base_price": 599.99, "stock": 35},
            {"name": "Racing Drone", "base_price": 399.99, "stock": 50},
            {"name": "Toy Drone", "base_price": 99.99, "stock": 100},
            {"name": "Professional Drone", "base_price": 1299.99, "stock": 20},
            {"name": "Mini Drone", "base_price": 149.99, "stock": 80}
        ],
        
        # Automobiles
        "Cars": [
            {"name": "Sedan Car", "base_price": 25000.00, "stock": 10},
            {"name": "SUV Vehicle", "base_price": 35000.00, "stock": 8},
            {"name": "Hatchback Car", "base_price": 20000.00, "stock": 12},
            {"name": "Luxury Car", "base_price": 50000.00, "stock": 5},
            {"name": "Compact Car", "base_price": 18000.00, "stock": 15}
        ],
        "Bikes": [
            {"name": "Sports Bike", "base_price": 15000.00, "stock": 20},
            {"name": "Cruiser Bike", "base_price": 12000.00, "stock": 25},
            {"name": "Commuter Bike", "base_price": 8000.00, "stock": 40},
            {"name": "Adventure Bike", "base_price": 20000.00, "stock": 15},
            {"name": "Electric Bike", "base_price": 18000.00, "stock": 18}
        ],
        "Electric Scooters": [
            {"name": "Electric Scooter", "base_price": 999.99, "stock": 50},
            {"name": "Folding Scooter", "base_price": 1299.99, "stock": 40},
            {"name": "Off-road Scooter", "base_price": 1499.99, "stock": 30},
            {"name": "City Scooter", "base_price": 799.99, "stock": 60},
            {"name": "Premium Scooter", "base_price": 1999.99, "stock": 25}
        ],
        "Car Accessories": [
            {"name": "Car Cover", "base_price": 89.99, "stock": 100},
            {"name": "Car Mats", "base_price": 49.99, "stock": 150},
            {"name": "Air Freshener", "base_price": 19.99, "stock": 200},
            {"name": "Car Organizer", "base_price": 39.99, "stock": 120},
            {"name": "Car Charger", "base_price": 29.99, "stock": 180}
        ],
        "Tyres": [
            {"name": "All Season Tyres", "base_price": 199.99, "stock": 80},
            {"name": "Summer Tyres", "base_price": 179.99, "stock": 90},
            {"name": "Winter Tyres", "base_price": 219.99, "stock": 70},
            {"name": "Performance Tyres", "base_price": 299.99, "stock": 50},
            {"name": "Off-road Tyres", "base_price": 249.99, "stock": 60}
        ],
        "Car Batteries": [
            {"name": "Car Battery", "base_price": 149.99, "stock": 60},
            {"name": "Heavy Duty Battery", "base_price": 199.99, "stock": 45},
            {"name": "Maintenance Free Battery", "base_price": 179.99, "stock": 55},
            {"name": "Deep Cycle Battery", "base_price": 249.99, "stock": 35},
            {"name": "Gel Battery", "base_price": 299.99, "stock": 30}
        ],
        "Motorbike Helmets": [
            {"name": "Full Face Helmet", "base_price": 199.99, "stock": 80},
            {"name": "Half Face Helmet", "base_price": 149.99, "stock": 100},
            {"name": "Modular Helmet", "base_price": 299.99, "stock": 50},
            {"name": "Off-road Helmet", "base_price": 249.99, "stock": 60},
            {"name": "Open Face Helmet", "base_price": 129.99, "stock": 90}
        ],
        "Car Audio Systems": [
            {"name": "Car Stereo", "base_price": 299.99, "stock": 50},
            {"name": "Car Speakers", "base_price": 199.99, "stock": 70},
            {"name": "Car Subwoofer", "base_price": 399.99, "stock": 40},
            {"name": "Car Amplifier", "base_price": 349.99, "stock": 45},
            {"name": "Car Audio System", "base_price": 599.99, "stock": 30}
        ],
        "Truck Parts": [
            {"name": "Truck Engine Part", "base_price": 499.99, "stock": 25},
            {"name": "Truck Brake System", "base_price": 399.99, "stock": 35},
            {"name": "Truck Suspension", "base_price": 599.99, "stock": 20},
            {"name": "Truck Transmission", "base_price": 899.99, "stock": 15},
            {"name": "Truck Electrical", "base_price": 299.99, "stock": 40}
        ],
        "SUV Accessories": [
            {"name": "Roof Rack", "base_price": 299.99, "stock": 50},
            {"name": "Towing Hook", "base_price": 199.99, "stock": 70},
            {"name": "SUV Cargo Organizer", "base_price": 149.99, "stock": 80},
            {"name": "SUV Floor Mats", "base_price": 89.99, "stock": 100},
            {"name": "SUV Seat Covers", "base_price": 179.99, "stock": 60}
        ],
        
        # Clothing
        "Men's T-Shirts": [
            {"name": "Cotton T-Shirt", "base_price": 24.99, "stock": 200},
            {"name": "Polo T-Shirt", "base_price": 34.99, "stock": 150},
            {"name": "Graphic T-Shirt", "base_price": 29.99, "stock": 180},
            {"name": "Sports T-Shirt", "base_price": 39.99, "stock": 120},
            {"name": "V-Neck T-Shirt", "base_price": 27.99, "stock": 160}
        ],
        "Women's Dresses": [
            {"name": "Summer Dress", "base_price": 59.99, "stock": 100},
            {"name": "Evening Dress", "base_price": 89.99, "stock": 80},
            {"name": "Casual Dress", "base_price": 49.99, "stock": 120},
            {"name": "Party Dress", "base_price": 79.99, "stock": 90},
            {"name": "Maxi Dress", "base_price": 69.99, "stock": 110}
        ],
        "Men's Jeans": [
            {"name": "Slim Fit Jeans", "base_price": 79.99, "stock": 150},
            {"name": "Straight Leg Jeans", "base_price": 69.99, "stock": 180},
            {"name": "Relaxed Fit Jeans", "base_price": 74.99, "stock": 160},
            {"name": "Skinny Jeans", "base_price": 84.99, "stock": 140},
            {"name": "Bootcut Jeans", "base_price": 79.99, "stock": 150}
        ],
        "Women's Tops": [
            {"name": "Blouse", "base_price": 44.99, "stock": 120},
            {"name": "Tank Top", "base_price": 24.99, "stock": 200},
            {"name": "Crop Top", "base_price": 29.99, "stock": 180},
            {"name": "Tunic Top", "base_price": 54.99, "stock": 100},
            {"name": "Peplum Top", "base_price": 49.99, "stock": 110}
        ],
        "Children's Clothing": [
            {"name": "Kids T-Shirt", "base_price": 19.99, "stock": 250},
            {"name": "Kids Dress", "base_price": 34.99, "stock": 150},
            {"name": "Kids Jeans", "base_price": 39.99, "stock": 180},
            {"name": "Kids Sweater", "base_price": 29.99, "stock": 200},
            {"name": "Kids Jacket", "base_price": 49.99, "stock": 120}
        ],
        "Footwear": [
            {"name": "Running Shoes", "base_price": 89.99, "stock": 100},
            {"name": "Casual Shoes", "base_price": 69.99, "stock": 150},
            {"name": "Formal Shoes", "base_price": 119.99, "stock": 80},
            {"name": "Sports Shoes", "base_price": 79.99, "stock": 120},
            {"name": "Sandals", "base_price": 49.99, "stock": 180}
        ],
        "Winter Jackets": [
            {"name": "Down Jacket", "base_price": 199.99, "stock": 60},
            {"name": "Puffer Jacket", "base_price": 149.99, "stock": 80},
            {"name": "Wool Jacket", "base_price": 179.99, "stock": 70},
            {"name": "Fleece Jacket", "base_price": 89.99, "stock": 100},
            {"name": "Bomber Jacket", "base_price": 129.99, "stock": 90}
        ],
        "Socks": [
            {"name": "Cotton Socks", "base_price": 9.99, "stock": 300},
            {"name": "Wool Socks", "base_price": 14.99, "stock": 250},
            {"name": "Sports Socks", "base_price": 12.99, "stock": 280},
            {"name": "Dress Socks", "base_price": 11.99, "stock": 290},
            {"name": "Ankle Socks", "base_price": 8.99, "stock": 320}
        ],
        "Caps and Hats": [
            {"name": "Baseball Cap", "base_price": 24.99, "stock": 200},
            {"name": "Beanie Hat", "base_price": 19.99, "stock": 250},
            {"name": "Fedora Hat", "base_price": 34.99, "stock": 150},
            {"name": "Bucket Hat", "base_price": 22.99, "stock": 180},
            {"name": "Visor Cap", "base_price": 18.99, "stock": 220}
        ],
        "Belts": [
            {"name": "Leather Belt", "base_price": 39.99, "stock": 120},
            {"name": "Casual Belt", "base_price": 29.99, "stock": 180},
            {"name": "Formal Belt", "base_price": 49.99, "stock": 100},
            {"name": "Braided Belt", "base_price": 34.99, "stock": 150},
            {"name": "Reversible Belt", "base_price": 44.99, "stock": 110}
        ]
    }
    
    # Get category name
    category_name = category.name
    
    # Get template for this category or use default
    if category_name in product_templates:
        template = product_templates[category_name][product_number - 1]
    else:
        # Default template for other categories
        template = {
            "name": f"{category_name} Product {product_number}",
            "base_price": round(random.uniform(50, 500), 2),
            "stock": random.randint(20, 100)
        }
    
    # Generate description
    descriptions = [
        f"High-quality {category_name.lower()} from {brand.name}. Perfect for everyday use.",
        f"Premium {category_name.lower()} featuring {brand.name} quality. Great value for money.",
        f"Reliable {category_name.lower()} by {brand.name}. Built to last.",
        f"Modern {category_name.lower()} with {brand.name} technology. Excellent performance.",
        f"Stylish {category_name.lower()} from {brand.name}. Perfect addition to your collection."
    ]
    
    return {
        "name": f"{brand.name} {template['name']}",
        "description": descriptions[product_number - 1],
        "base_price": template["base_price"],
        "stock": template["stock"],
        "discount_percentage": random.choice([0, 5, 10, 15, 20]) if random.random() < 0.3 else 0,
        "condition": random.choice(ProductCondition.choices)[0]
    }

def create_product(seller, product_number):
    """Create a product for the seller"""
    category, brand = get_random_category_and_brand()
    product_data = generate_product_data(category, brand, product_number)
    
    # Calculate final price
    final_price = product_data["base_price"]
    if product_data["discount_percentage"] > 0:
        discount_amount = product_data["base_price"] * (product_data["discount_percentage"] / 100)
        final_price = product_data["base_price"] - discount_amount
    
    product = Product.objects.create(
        seller=seller,
        category=category,
        brand=brand,
        name=product_data["name"],
        description=product_data["description"],
        base_price=product_data["base_price"],
        discount_percentage=product_data["discount_percentage"],
        final_price=final_price,
        stock=product_data["stock"],
        condition=product_data["condition"]
    )
    
    return product

def main():
    """Main function to populate sellers and products"""
    print("Starting to populate database with sellers and products...")
    print("=" * 60)
    
    # Check if categories and brands exist
    if not Category.objects.exists():
        print("❌ No categories found. Please run category population scripts first.")
        return
    
    if not Brand.objects.exists():
        print("❌ No brands found. Please run brand population script first.")
        return
    
    # Create 20 sellers
    sellers = []
    for i in range(1, 21):
        seller = create_user_and_seller(i)
        sellers.append(seller)
    
    print(f"\n✅ Successfully created {len(sellers)} seller accounts")
    print("=" * 60)
    
    # Create 5 products for each seller
    total_products = 0
    for seller in sellers:
        print(f"\nCreating products for {seller.shop_name}...")
        
        for product_num in range(1, 6):
            try:
                product = create_product(seller, product_num)
                print(f"  ✓ Created: {product.name} - ${product.base_price}")
                total_products += 1
            except Exception as e:
                print(f"  ❌ Error creating product {product_num}: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully created {len(sellers)} seller accounts")
    print(f"✅ Successfully created {total_products} products")
    print(f"📊 Average products per seller: {total_products / len(sellers):.1f}")
    print("=" * 60)
    
    # Print summary statistics
    print("\n📈 Database Summary:")
    print(f"   • Total Users: {User.objects.count()}")
    print(f"   • Total Sellers: {Seller.objects.count()}")
    print(f"   • Total Products: {Product.objects.count()}")
    print(f"   • Total Categories: {Category.objects.count()}")
    print(f"   • Total Brands: {Brand.objects.count()}")
    
    # Print sample products
    print("\n🛍️ Sample Products Created:")
    sample_products = Product.objects.all()[:10]
    for product in sample_products:
        print(f"   • {product.name} - ${product.base_price} ({product.seller.shop_name})")

if __name__ == "__main__":
    main() 