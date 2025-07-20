#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Category, CategoryAttribute, AttributeOption

def fix_category_attributes():
    print("=== Fixing Category Attributes ===")
    
    # Get main categories
    clothing = Category.objects.filter(name='Clothing').first()
    electronics = Category.objects.filter(name='Electronics').first()
    
    if not clothing or not electronics:
        print("Main categories not found!")
        return
    
    print(f"Clothing category ID: {clothing.id}")
    print(f"Electronics category ID: {electronics.id}")
    
    # Create attributes for Clothing category
    print("\nCreating attributes for Clothing category...")
    
    # Size attribute
    size_attr, created = CategoryAttribute.objects.get_or_create(
        name='Size',
        category=clothing,
        defaults={
            'input_type': 'dropdown',
            'is_required': True,
            'unit': None
        }
    )
    print(f"Size attribute: {'Created' if created else 'Already exists'}")
    
    # Color attribute
    color_attr, created = CategoryAttribute.objects.get_or_create(
        name='Color',
        category=clothing,
        defaults={
            'input_type': 'text',
            'is_required': True,
            'unit': None
        }
    )
    print(f"Color attribute: {'Created' if created else 'Already exists'}")
    
    # Material attribute
    material_attr, created = CategoryAttribute.objects.get_or_create(
        name='Material',
        category=clothing,
        defaults={
            'input_type': 'text',
            'is_required': False,
            'unit': None
        }
    )
    print(f"Material attribute: {'Created' if created else 'Already exists'}")
    
    # Create attributes for Electronics category
    print("\nCreating attributes for Electronics category...")
    
    # Brand attribute
    brand_attr, created = CategoryAttribute.objects.get_or_create(
        name='Brand',
        category=electronics,
        defaults={
            'input_type': 'dropdown',
            'is_required': True,
            'unit': None
        }
    )
    print(f"Brand attribute: {'Created' if created else 'Already exists'}")
    
    # Model attribute
    model_attr, created = CategoryAttribute.objects.get_or_create(
        name='Model',
        category=electronics,
        defaults={
            'input_type': 'text',
            'is_required': True,
            'unit': None
        }
    )
    print(f"Model attribute: {'Created' if created else 'Already exists'}")
    
    # Warranty attribute
    warranty_attr, created = CategoryAttribute.objects.get_or_create(
        name='Warranty',
        category=electronics,
        defaults={
            'input_type': 'dropdown',
            'is_required': False,
            'unit': None
        }
    )
    print(f"Warranty attribute: {'Created' if created else 'Already exists'}")
    
    # Create options for Clothing attributes
    print("\nCreating options for Clothing attributes...")
    
    # Size options
    size_options = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    for size in size_options:
        AttributeOption.objects.get_or_create(
            attribute=size_attr,
            value=size
        )
    print(f"Created {len(size_options)} size options")
    
    # Color options
    color_options = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Gray']
    for color in color_options:
        AttributeOption.objects.get_or_create(
            attribute=color_attr,
            value=color
        )
    print(f"Created {len(color_options)} color options")
    
    # Material options
    material_options = ['Cotton', 'Polyester', 'Wool', 'Silk', 'Linen', 'Denim', 'Leather', 'Synthetic', 'Bamboo', 'Hemp']
    for material in material_options:
        AttributeOption.objects.get_or_create(
            attribute=material_attr,
            value=material
        )
    print(f"Created {len(material_options)} material options")
    
    # Create options for Electronics attributes
    print("\nCreating options for Electronics attributes...")
    
    # Brand options
    brand_options = ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Microsoft', 'Google', 'Xiaomi']
    for brand in brand_options:
        AttributeOption.objects.get_or_create(
            attribute=brand_attr,
            value=brand
        )
    print(f"Created {len(brand_options)} brand options")
    
    # Model options
    model_options = ['iPhone 15', 'Galaxy S24', 'MacBook Pro', 'ThinkPad X1', 'Surface Pro', 'iPad Pro', 'AirPods Pro', 'Galaxy Tab', 'MacBook Air', 'Dell XPS']
    for model in model_options:
        AttributeOption.objects.get_or_create(
            attribute=model_attr,
            value=model
        )
    print(f"Created {len(model_options)} model options")
    
    # Warranty options
    warranty_options = ['1 Year', '2 Years', '3 Years', '5 Years', 'Lifetime', 'No Warranty', 'Extended Warranty']
    for warranty in warranty_options:
        AttributeOption.objects.get_or_create(
            attribute=warranty_attr,
            value=warranty
        )
    print(f"Created {len(warranty_options)} warranty options")
    
    print("\n=== Verification ===")
    
    # Verify Clothing attributes
    clothing_attrs = CategoryAttribute.objects.filter(category=clothing)
    print(f"Clothing category has {clothing_attrs.count()} attributes:")
    for attr in clothing_attrs:
        opts = AttributeOption.objects.filter(attribute=attr)
        print(f"- {attr.name} ({attr.input_type}): {opts.count()} options")
    
    # Verify Electronics attributes
    electronics_attrs = CategoryAttribute.objects.filter(category=electronics)
    print(f"\nElectronics category has {electronics_attrs.count()} attributes:")
    for attr in electronics_attrs:
        opts = AttributeOption.objects.filter(attribute=attr)
        print(f"- {attr.name} ({attr.input_type}): {opts.count()} options")
    
    print("\n✅ Category attributes fixed successfully!")

if __name__ == "__main__":
    fix_category_attributes() 