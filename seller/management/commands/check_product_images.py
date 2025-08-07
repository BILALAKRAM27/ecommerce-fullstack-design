#!/usr/bin/env python
"""
Script to check and display information about existing product images
Run this script from the Django project root directory
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Product, ProductImage, Category

def main():
    """Main function to check product images"""
    print("Checking existing product images in MarketVibe database...")
    print("=" * 60)
    
    # Get all products
    products = Product.objects.all()
    total_products = products.count()
    
    print(f"Total Products: {total_products}")
    
    # Get products with images
    products_with_images = Product.objects.filter(images__isnull=False).distinct()
    products_with_images_count = products_with_images.count()
    
    print(f"Products with Images: {products_with_images_count}")
    
    # Get total image count
    total_images = ProductImage.objects.count()
    thumbnail_images = ProductImage.objects.filter(is_thumbnail=True).count()
    
    print(f"Total Product Images: {total_images}")
    print(f"Thumbnail Images: {thumbnail_images}")
    print(f"Additional Images: {total_images - thumbnail_images}")
    
    if total_products > 0:
        print(f"Average images per product: {total_images / total_products:.1f}")
    
    print("\n" + "=" * 60)
    print("📊 DETAILED BREAKDOWN")
    print("=" * 60)
    
    # Show products by category
    categories = Category.objects.all()
    for category in categories:
        category_products = products.filter(category=category)
        category_products_with_images = category_products.filter(images__isnull=False).distinct()
        
        if category_products.exists():
            print(f"\n{category.name}:")
            print(f"  • Total products: {category_products.count()}")
            print(f"  • Products with images: {category_products_with_images.count()}")
            
            # Show sample products from this category
            sample_products = category_products_with_images[:3]
            for product in sample_products:
                image_count = product.images.count()
                has_thumbnail = product.images.filter(is_thumbnail=True).exists()
                print(f"    - {product.name}: {image_count} images" + 
                      (" ✓" if has_thumbnail else " ✗"))
    
    print("\n" + "=" * 60)
    print("🖼️ SAMPLE PRODUCTS WITH IMAGES")
    print("=" * 60)
    
    # Show detailed sample of products with images
    sample_products = products_with_images[:10]
    for i, product in enumerate(sample_products, 1):
        image_count = product.images.count()
        thumbnail = product.images.filter(is_thumbnail=True).first()
        additional_images = product.images.filter(is_thumbnail=False).count()
        
        print(f"\n{i}. {product.name}")
        print(f"   Category: {product.category.name}")
        print(f"   Seller: {product.seller.shop_name}")
        print(f"   Price: ${product.base_price}")
        print(f"   Images: {image_count} total")
        print(f"   - Thumbnail: {'✓' if thumbnail else '✗'}")
        print(f"   - Additional: {additional_images}")
        
        if thumbnail:
            print(f"   - Thumbnail ID: {thumbnail.id}")
    
    print("\n" + "=" * 60)
    print("✅ IMAGE STATUS SUMMARY")
    print("=" * 60)
    
    if products_with_images_count == total_products:
        print("🎉 All products have images!")
    else:
        print(f"⚠️  {total_products - products_with_images_count} products still need images")
    
    if thumbnail_images == products_with_images_count:
        print("🎉 All products with images have thumbnails!")
    else:
        print(f"⚠️  {products_with_images_count - thumbnail_images} products missing thumbnails")
    
    print(f"\n📈 Coverage: {products_with_images_count}/{total_products} products ({products_with_images_count/total_products*100:.1f}%)")
    print(f"📈 Thumbnail coverage: {thumbnail_images}/{products_with_images_count} products ({thumbnail_images/products_with_images_count*100:.1f}%)")

if __name__ == "__main__":
    main() 