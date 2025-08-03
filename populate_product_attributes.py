#!/usr/bin/env python
"""
Script to populate MarketVibe database with Product Attribute Values
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

from seller.models import Product, CategoryAttribute, ProductAttributeValue, AttributeOption, InputType

def generate_attribute_value(attribute, product_name):
    """Generate appropriate attribute value based on attribute type and product"""
    
    # Get attribute options if it's a dropdown
    if attribute.input_type == InputType.DROPDOWN:
        options = attribute.options.all()
        if options.exists():
            return random.choice(options).value
        else:
            return "Default"
    
    # Generate values based on attribute name and type
    attribute_name = attribute.name.lower()
    
    if attribute.input_type == InputType.NUMBER:
        # Generate realistic numbers based on attribute name
        if "ram" in attribute_name:
            return str(random.choice([4, 6, 8, 12, 16]))
        elif "storage" in attribute_name or "capacity" in attribute_name:
            return str(random.choice([64, 128, 256, 512, 1024]))
        elif "battery" in attribute_name:
            return str(random.choice([3000, 4000, 5000, 6000, 7000]))
        elif "screen" in attribute_name or "size" in attribute_name:
            return str(random.choice([5, 6, 7, 8, 10, 13, 15, 17]))
        elif "weight" in attribute_name:
            return str(random.choice([100, 150, 200, 250, 300, 500]))
        elif "length" in attribute_name or "height" in attribute_name:
            return str(random.choice([10, 15, 20, 25, 30, 40, 50]))
        elif "width" in attribute_name:
            return str(random.choice([5, 8, 10, 12, 15, 20]))
        elif "thickness" in attribute_name:
            return str(random.choice([2, 3, 5, 8, 10, 12]))
        elif "voltage" in attribute_name:
            return str(random.choice([12, 24, 48, 110, 220]))
        elif "power" in attribute_name or "wattage" in attribute_name:
            return str(random.choice([50, 100, 200, 300, 500, 1000]))
        elif "speed" in attribute_name:
            return str(random.choice([100, 200, 300, 500, 1000]))
        elif "pressure" in attribute_name:
            return str(random.choice([10, 20, 30, 50, 100]))
        elif "temperature" in attribute_name:
            return str(random.choice([20, 25, 30, 35, 40]))
        elif "frequency" in attribute_name:
            return str(random.choice([50, 60, 100, 200, 500]))
        elif "current" in attribute_name or "amps" in attribute_name:
            return str(random.choice([1, 2, 5, 10, 15, 20]))
        elif "flow" in attribute_name:
            return str(random.choice([10, 20, 50, 100, 200]))
        elif "capacity" in attribute_name:
            return str(random.choice([1, 2, 5, 10, 20, 50]))
        else:
            return str(random.randint(1, 100))
    
    elif attribute.input_type == InputType.BOOLEAN:
        # Generate Yes/No based on attribute name
        if any(word in attribute_name for word in ["waterproof", "wireless", "bluetooth", "wifi", "smart", "touch", "backlit", "adjustable", "foldable", "recliner", "storage", "lockable", "framed", "retractable", "washable", "airline", "certified", "magnetic", "auto", "gps", "fast", "solar", "reversible", "universal", "hooded", "non-slip", "scented"]):
            return random.choice(["Yes", "No"])
        else:
            return random.choice(["Yes", "No"])
    
    elif attribute.input_type == InputType.TEXT:
        # Generate text based on attribute name
        if "brand" in attribute_name:
            return product_name.split()[0] if product_name else "Generic"
        elif "color" in attribute_name:
            return random.choice(["Black", "White", "Blue", "Red", "Green", "Silver", "Gold", "Gray", "Brown", "Pink"])
        elif "material" in attribute_name:
            return random.choice(["Plastic", "Metal", "Wood", "Glass", "Fabric", "Leather", "Rubber", "Aluminum", "Steel", "Carbon Fiber"])
        elif "type" in attribute_name:
            return random.choice(["Standard", "Premium", "Professional", "Basic", "Advanced", "Compact", "Portable", "Fixed"])
        elif "style" in attribute_name:
            return random.choice(["Modern", "Classic", "Vintage", "Contemporary", "Traditional", "Minimalist", "Luxury"])
        elif "pattern" in attribute_name:
            return random.choice(["Solid", "Striped", "Floral", "Geometric", "Abstract", "Plain", "Printed"])
        elif "connection" in attribute_name:
            return random.choice(["Wired", "Wireless", "Bluetooth", "USB", "HDMI", "WiFi"])
        elif "source" in attribute_name:
            return random.choice(["LED", "LCD", "OLED", "CFL", "Halogen", "Incandescent"])
        elif "fuel" in attribute_name:
            return random.choice(["Petrol", "Diesel", "Electric", "Hybrid", "Gas", "Battery"])
        elif "transmission" in attribute_name:
            return random.choice(["Manual", "Automatic", "CVT", "Semi-Auto"])
        elif "fit" in attribute_name:
            return random.choice(["Slim", "Regular", "Loose", "Skinny", "Relaxed", "Standard"])
        elif "wash" in attribute_name:
            return random.choice(["Light", "Medium", "Dark", "Stone", "Acid", "Regular"])
        elif "neck" in attribute_name:
            return random.choice(["Round", "V-neck", "Collar", "Boat", "Crew", "Scoop"])
        elif "sleeve" in attribute_name:
            return random.choice(["Full", "Half", "3/4th", "Sleeveless", "Short", "Long"])
        elif "sole" in attribute_name:
            return random.choice(["Rubber", "EVA", "PU", "Leather", "Synthetic"])
        elif "strap" in attribute_name:
            return random.choice(["Velcro", "Lace-up", "Elastic", "Buckle", "Hook"])
        elif "buckle" in attribute_name:
            return random.choice(["Pin", "Automatic", "Reversible", "Standard", "Quick-release"])
        elif "stud" in attribute_name:
            return random.choice(["Firm Ground", "Soft Ground", "Turf", "Indoor", "Artificial"])
        elif "willow" in attribute_name:
            return random.choice(["English", "Kashmir", "Premium", "Standard"])
        elif "panel" in attribute_name:
            return random.choice(["IPS", "TN", "VA", "OLED", "QLED"])
        elif "resolution" in attribute_name:
            return random.choice(["HD", "Full HD", "2K", "4K", "8K", "720p", "1080p"])
        elif "dpi" in attribute_name:
            return random.choice(["800-1600", "1600-3200", "3200-6400", "1000-2000"])
        elif "function" in attribute_name:
            return random.choice(["Print", "Print + Scan", "All-in-One", "Copy", "Fax"])
        elif "band" in attribute_name:
            return random.choice(["Single", "Dual", "Tri-band", "2.4GHz", "5GHz"])
        elif "connection" in attribute_name:
            return random.choice(["USB 2.0", "3.0", "Type-C", "Thunderbolt", "FireWire"])
        elif "mount" in attribute_name:
            return random.choice(["Clip-on", "Tripod", "Wall", "Ceiling", "Table"])
        elif "channel" in attribute_name:
            return random.choice(["2.0", "2.1", "5.1", "7.1", "Stereo", "Mono"])
        elif "license" in attribute_name:
            return random.choice(["1 Year", "3 Years", "Lifetime", "Perpetual", "Subscription"])
        elif "platform" in attribute_name:
            return random.choice(["Windows", "Mac", "Linux", "Cross-platform", "Mobile"])
        elif "type" in attribute_name:
            return random.choice(["Corded", "Cordless", "Battery", "Electric", "Manual"])
        elif "phase" in attribute_name:
            return random.choice(["Single", "Three", "Dual", "Multi"])
        elif "control" in attribute_name:
            return random.choice(["Manual", "Automatic", "Digital", "Analog", "Remote"])
        elif "engine" in attribute_name:
            return random.choice(["Petrol", "Diesel", "Electric", "Hybrid", "Gas"])
        elif "duty" in attribute_name:
            return random.choice(["Continuous", "Intermittent", "Heavy", "Light", "Standard"])
        elif "crane" in attribute_name:
            return random.choice(["Gantry", "Overhead", "Jib", "Mobile", "Tower"])
        elif "glass" in attribute_name:
            return random.choice(["Acrylic", "Glass", "Tempered", "Laminated", "Float"])
        elif "filter" in attribute_name:
            return random.choice(["Mechanical", "Biological", "Chemical", "UV", "Carbon"])
        elif "pump" in attribute_name:
            return random.choice(["Electric", "Diesel", "Solar", "Manual", "Submersible"])
        elif "vacuum" in attribute_name:
            return random.choice(["Wet & Dry", "Dry Only", "HEPA", "Bagless", "Cordless"])
        elif "generator" in attribute_name:
            return random.choice(["Petrol", "Diesel", "Gas", "Solar", "Wind"])
        elif "handling" in attribute_name:
            return random.choice(["Gantry", "Overhead", "Jib", "Mobile", "Tower"])
        else:
            return "Standard"

def populate_product_attributes():
    """Populate product attributes for all products"""
    print("Starting to populate Product Attribute Values...")
    print("=" * 60)
    
    # Check prerequisites
    if not Product.objects.exists():
        print("❌ No products found. Please run product population script first.")
        return
    
    if not CategoryAttribute.objects.exists():
        print("❌ No category attributes found. Please run category population scripts first.")
        return
    
    # Get all products
    products = Product.objects.all()
    total_products = products.count()
    
    print(f"📦 Found {total_products} products to populate with attributes")
    
    # Track statistics
    total_attributes_created = 0
    products_with_attributes = 0
    
    for i, product in enumerate(products, 1):
        print(f"\nProcessing product {i}/{total_products}: {product.name}")
        
        # Get category attributes for this product's category
        category_attributes = CategoryAttribute.objects.filter(category=product.category)
        
        if not category_attributes.exists():
            print(f"  ⚠️ No attributes found for category: {product.category.name}")
            continue
        
        attributes_created = 0
        
        for attribute in category_attributes:
            # Generate appropriate value for this attribute
            value = generate_attribute_value(attribute, product.name)
            
            # Create or update the attribute value
            attr_value, created = ProductAttributeValue.objects.get_or_create(
                product=product,
                attribute=attribute,
                defaults={'value': value}
            )
            
            if created:
                attributes_created += 1
                print(f"  ✓ {attribute.name}: {value}")
            else:
                # Update existing value
                attr_value.value = value
                attr_value.save()
                print(f"  ↻ {attribute.name}: {value}")
        
        total_attributes_created += attributes_created
        if attributes_created > 0:
            products_with_attributes += 1
        
        print(f"  📊 Created {attributes_created} attributes for this product")
    
    # Print summary
    print("\n" + "=" * 60)
    print("✅ Product Attribute Values populated successfully!")
    print("=" * 60)
    
    print(f"\n📈 Summary:")
    print(f"   • Total Products Processed: {total_products}")
    print(f"   • Products with Attributes: {products_with_attributes}")
    print(f"   • Total Attribute Values Created: {total_attributes_created}")
    print(f"   • Average Attributes per Product: {total_attributes_created / total_products:.1f}")
    
    # Print sample data
    print(f"\n🔍 Sample Attribute Values:")
    sample_products = Product.objects.all()[:5]
    for product in sample_products:
        attributes = product.attribute_values.all()
        if attributes.exists():
            print(f"   • {product.name}:")
            for attr in attributes[:3]:  # Show first 3 attributes
                print(f"     - {attr.attribute.name}: {attr.value}")
        else:
            print(f"   • {product.name}: No attributes")

def validate_attribute_data():
    """Validate that attribute data is properly created"""
    print("\n🔍 Validating Attribute Data...")
    
    # Check total attribute values
    total_attr_values = ProductAttributeValue.objects.count()
    print(f"✓ Total Attribute Values: {total_attr_values}")
    
    # Check products with attributes
    products_with_attrs = Product.objects.filter(attribute_values__isnull=False).distinct().count()
    total_products = Product.objects.count()
    print(f"✓ Products with Attributes: {products_with_attrs}/{total_products}")
    
    # Check attribute distribution
    print("\n📊 Attribute Distribution by Category:")
    categories = CategoryAttribute.objects.values_list('category__name', flat=True).distinct()
    
    for category_name in categories:
        category_attrs = CategoryAttribute.objects.filter(category__name=category_name)
        products_in_category = Product.objects.filter(category__name=category_name)
        attr_values_in_category = ProductAttributeValue.objects.filter(
            attribute__category__name=category_name
        ).count()
        
        print(f"   • {category_name}: {attr_values_in_category} values for {products_in_category.count()} products")
    
    # Check attribute types
    print("\n📋 Attribute Types Distribution:")
    attr_types = ProductAttributeValue.objects.values_list('attribute__input_type', flat=True).distinct()
    
    for attr_type in attr_types:
        count = ProductAttributeValue.objects.filter(attribute__input_type=attr_type).count()
        print(f"   • {attr_type}: {count} values")

def main():
    """Main function to populate product attributes"""
    print("Starting to populate Product Attribute Values...")
    print("=" * 60)
    
    # Populate attributes
    populate_product_attributes()
    
    # Validate data
    validate_attribute_data()
    
    print("\n" + "=" * 60)
    print("✅ Product Attribute Values population completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 