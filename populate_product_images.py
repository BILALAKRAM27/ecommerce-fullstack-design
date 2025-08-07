#!/usr/bin/env python
"""
Script to populate MarketVibe database with product images
Run this script from the Django project root directory
"""

import os
import sys
import django
import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import uuid

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Product, ProductImage, Category, Brand

def create_sample_image(width=400, height=300, text="Product Image", bg_color=None, text_color=None):
    """Create a sample product image with text"""
    if bg_color is None:
        bg_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    if text_color is None:
        text_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    
    # Create image
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font, fallback to default if not available
    try:
        # Try to use a larger font size
        font_size = min(width, height) // 10
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Calculate text position (center)
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(text) * 10
        text_height = 20
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text
    if font:
        draw.text((x, y), text, fill=text_color, font=font)
    else:
        draw.text((x, y), text, fill=text_color)
    
    # Add some decorative elements
    # Draw a border
    draw.rectangle([0, 0, width-1, height-1], outline=text_color, width=2)
    
    # Add some random decorative circles
    for _ in range(3):
        circle_x = random.randint(20, width-20)
        circle_y = random.randint(20, height-20)
        circle_size = random.randint(5, 15)
        draw.ellipse([circle_x, circle_y, circle_x+circle_size, circle_y+circle_size], 
                    fill=text_color, outline=bg_color)
    
    return image

def create_category_specific_image(category_name, product_name, width=400, height=300):
    """Create category-specific product images"""
    
    # Define category-specific colors and styles
    category_styles = {
        # Electronics
        "Smartphones": {"bg": (25, 118, 210), "text": (255, 255, 255), "icon": "📱"},
        "Laptops": {"bg": (0, 150, 136), "text": (255, 255, 255), "icon": "💻"},
        "Smart Watches": {"bg": (156, 39, 176), "text": (255, 255, 255), "icon": "⌚"},
        "LED TVs": {"bg": (33, 33, 33), "text": (255, 255, 255), "icon": "📺"},
        "Bluetooth Speakers": {"bg": (255, 152, 0), "text": (255, 255, 255), "icon": "🔊"},
        "Cameras": {"bg": (76, 175, 80), "text": (255, 255, 255), "icon": "📷"},
        "Headphones": {"bg": (121, 85, 72), "text": (255, 255, 255), "icon": "🎧"},
        "Power Banks": {"bg": (255, 193, 7), "text": (0, 0, 0), "icon": "🔋"},
        "Gaming Consoles": {"bg": (233, 30, 99), "text": (255, 255, 255), "icon": "🎮"},
        "Drones": {"bg": (63, 81, 181), "text": (255, 255, 255), "icon": "🚁"},
        
        # Automobiles
        "Cars": {"bg": (244, 67, 54), "text": (255, 255, 255), "icon": "🚗"},
        "Bikes": {"bg": (255, 87, 34), "text": (255, 255, 255), "icon": "🏍️"},
        "Electric Scooters": {"bg": (0, 188, 212), "text": (255, 255, 255), "icon": "🛴"},
        "Car Accessories": {"bg": (158, 158, 158), "text": (255, 255, 255), "icon": "🔧"},
        "Tyres": {"bg": (96, 125, 139), "text": (255, 255, 255), "icon": "🛞"},
        "Car Batteries": {"bg": (255, 235, 59), "text": (0, 0, 0), "icon": "⚡"},
        "Motorbike Helmets": {"bg": (255, 111, 0), "text": (255, 255, 255), "icon": "🪖"},
        "Car Audio Systems": {"bg": (103, 58, 183), "text": (255, 255, 255), "icon": "🎵"},
        "Truck Parts": {"bg": (139, 69, 19), "text": (255, 255, 255), "icon": "🚛"},
        "SUV Accessories": {"bg": (165, 42, 42), "text": (255, 255, 255), "icon": "🚙"},
        
        # Clothing
        "Men's T-Shirts": {"bg": (30, 136, 229), "text": (255, 255, 255), "icon": "👕"},
        "Women's Dresses": {"bg": (233, 30, 99), "text": (255, 255, 255), "icon": "👗"},
        "Men's Jeans": {"bg": (63, 81, 181), "text": (255, 255, 255), "icon": "👖"},
        "Women's Tops": {"bg": (255, 64, 129), "text": (255, 255, 255), "icon": "👚"},
        "Children's Clothing": {"bg": (255, 193, 7), "text": (0, 0, 0), "icon": "👶"},
        "Footwear": {"bg": (121, 85, 72), "text": (255, 255, 255), "icon": "👟"},
        "Winter Jackets": {"bg": (33, 150, 243), "text": (255, 255, 255), "icon": "🧥"},
        "Socks": {"bg": (255, 255, 255), "text": (0, 0, 0), "icon": "🧦"},
        "Caps and Hats": {"bg": (255, 152, 0), "text": (255, 255, 255), "icon": "🧢"},
        "Belts": {"bg": (139, 69, 19), "text": (255, 255, 255), "icon": "👔"},
    }
    
    # Get style for this category or use default
    style = category_styles.get(category_name, {
        "bg": (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)),
        "text": (255, 255, 255),
        "icon": "📦"
    })
    
    # Create image with category-specific styling
    image = Image.new('RGB', (width, height), style["bg"])
    draw = ImageDraw.Draw(image)
    
    # Try to use a font
    try:
        font_size = min(width, height) // 8
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Create text with icon and product name
    display_text = f"{style['icon']} {product_name}"
    
    # Calculate text position
    if font:
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(display_text) * 10
        text_height = 20
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text
    if font:
        draw.text((x, y), display_text, fill=style["text"], font=font)
    else:
        draw.text((x, y), display_text, fill=style["text"])
    
    # Add border
    draw.rectangle([0, 0, width-1, height-1], outline=style["text"], width=3)
    
    # Add category label at bottom
    category_text = f"Category: {category_name}"
    if font:
        small_font = ImageFont.truetype("arial.ttf", font_size // 2)
    else:
        small_font = font
    
    if small_font:
        bbox = draw.textbbox((0, 0), category_text, font=small_font)
        cat_text_width = bbox[2] - bbox[0]
        cat_x = (width - cat_text_width) // 2
        cat_y = height - 40
        draw.text((cat_x, cat_y), category_text, fill=style["text"], font=small_font)
    
    return image

def image_to_binary(image):
    """Convert PIL image to binary data"""
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return buffer.getvalue()

def add_images_to_product(product, num_images=3):
    """Add multiple images to a product"""
    category_name = product.category.name
    product_name = product.name
    
    # Create different types of images
    images_created = 0
    
    # Main product image (thumbnail)
    main_image = create_category_specific_image(category_name, product_name, 500, 400)
    main_binary = image_to_binary(main_image)
    
    # Create ProductImage object for main image
    main_product_image = ProductImage.objects.create(
        product=product,
        image=main_binary,
        is_thumbnail=True
    )
    images_created += 1
    print(f"    ✓ Created thumbnail image")
    
    # Additional product images
    for i in range(1, num_images):
        # Create different angle/variant images
        if i == 1:
            # Side view
            angle_image = create_category_specific_image(category_name, f"{product_name} (Side View)", 450, 350)
        elif i == 2:
            # Detail view
            angle_image = create_category_specific_image(category_name, f"{product_name} (Detail)", 480, 380)
        else:
            # Generic additional image
            angle_image = create_category_specific_image(category_name, f"{product_name} (View {i+1})", 460, 360)
        
        angle_binary = image_to_binary(angle_image)
        
        # Create ProductImage object
        ProductImage.objects.create(
            product=product,
            image=angle_binary,
            is_thumbnail=False
        )
        images_created += 1
        print(f"    ✓ Created additional image {i}")
    
    return images_created

def update_product_main_image(product):
    """Update the main product image field"""
    # Get the thumbnail image
    thumbnail = product.images.filter(is_thumbnail=True).first()
    if thumbnail:
        product.set_image(thumbnail.image)
        product.save()
        print(f"    ✓ Updated main product image")
        return True
    return False

def main():
    """Main function to populate product images"""
    print("Starting to populate database with product images...")
    print("=" * 60)
    
    # Check if products exist
    products = Product.objects.all()
    if not products.exists():
        print("❌ No products found. Please run product population script first.")
        return
    
    print(f"Found {products.count()} products to process")
    print("=" * 60)
    
    total_images_created = 0
    products_processed = 0
    
    for product in products:
        print(f"\nProcessing: {product.name} ({product.category.name})")
        
        # Check if product already has images
        existing_images = product.images.count()
        if existing_images > 0:
            print(f"    ⚠️  Product already has {existing_images} images, skipping...")
            continue
        
        try:
            # Add 3 images per product (1 thumbnail + 2 additional)
            images_created = add_images_to_product(product, num_images=3)
            total_images_created += images_created
            
            # Update the main product image field
            update_product_main_image(product)
            
            products_processed += 1
            print(f"    ✅ Successfully added {images_created} images")
            
        except Exception as e:
            print(f"    ❌ Error processing product {product.name}: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully processed {products_processed} products")
    print(f"✅ Successfully created {total_images_created} product images")
    print(f"📊 Average images per product: {total_images_created / products_processed:.1f}" if products_processed > 0 else "📊 No products processed")
    print("=" * 60)
    
    # Print summary statistics
    print("\n📈 Database Summary:")
    print(f"   • Total Products: {Product.objects.count()}")
    print(f"   • Products with Images: {Product.objects.filter(images__isnull=False).distinct().count()}")
    print(f"   • Total Product Images: {ProductImage.objects.count()}")
    print(f"   • Thumbnail Images: {ProductImage.objects.filter(is_thumbnail=True).count()}")
    
    # Print sample products with images
    print("\n🖼️ Sample Products with Images:")
    sample_products = Product.objects.filter(images__isnull=False).distinct()[:5]
    for product in sample_products:
        image_count = product.images.count()
        thumbnail = product.images.filter(is_thumbnail=True).first()
        print(f"   • {product.name} - {image_count} images" + 
              (f" (thumbnail: {thumbnail.id})" if thumbnail else ""))

if __name__ == "__main__":
    main() 