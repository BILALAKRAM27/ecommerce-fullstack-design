#!/usr/bin/env python
"""
Script to populate MarketVibe database with Product Reviews and Seller Reviews
Run this script from the Django project root directory
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from django.utils import timezone
from buyer.models import Buyer
from seller.models import Seller, Product, ProductReview, SellerReview, ProductReviewLike, SellerReviewLike

def create_product_reviews():
    """Create product reviews from buyers"""
    print("Creating Product Reviews...")
    
    buyers = list(Buyer.objects.all())
    products = list(Product.objects.all())
    
    if not buyers:
        print("❌ No buyers found. Please run buyer population script first.")
        return []
    
    if not products:
        print("❌ No products found. Please run seller and product population script first.")
        return []
    
    # Review templates for different rating levels
    review_templates = {
        5.0: [
            "Excellent product! Exceeded my expectations. Highly recommend!",
            "Outstanding quality and fast delivery. Will definitely buy again!",
            "Perfect! The product is exactly as described and works flawlessly.",
            "Amazing value for money. Great quality and excellent service.",
            "Absolutely love this product! It's even better than expected.",
            "Top-notch quality and professional packaging. 5 stars!",
            "Fantastic product with excellent customer service. Highly satisfied!",
            "Outstanding! The quality is exceptional and delivery was prompt.",
            "Excellent purchase! The product is durable and well-made.",
            "Perfect product! Great price and excellent quality."
        ],
        4.5: [
            "Very good product with minor improvements possible.",
            "Great quality and good value for money. Recommended!",
            "Solid product that meets expectations. Good purchase.",
            "Good quality and reasonable price. Satisfied with the purchase.",
            "Nice product with good features. Would recommend.",
            "Good value for money. Quality is as expected.",
            "Satisfactory product with good performance.",
            "Decent quality and fair pricing. Good overall experience.",
            "Good product with minor issues. Still recommend.",
            "Solid purchase with good customer service."
        ],
        4.0: [
            "Good product overall. Meets basic expectations.",
            "Decent quality for the price. Satisfactory purchase.",
            "Acceptable product with room for improvement.",
            "Fair quality and reasonable price. Adequate for needs.",
            "Good enough for the price. No major complaints.",
            "Satisfactory product with standard quality.",
            "Decent purchase with acceptable quality.",
            "Reasonable product for the price point.",
            "Good basic product. Meets requirements.",
            "Acceptable quality and fair pricing."
        ],
        3.5: [
            "Average product with some issues. Could be better.",
            "Mediocre quality but functional. Not bad for the price.",
            "Okay product with minor problems. Acceptable.",
            "Average quality with room for improvement.",
            "Decent but not exceptional. Gets the job done.",
            "Fair product with some limitations.",
            "Acceptable quality with minor drawbacks.",
            "Average performance. Could be improved.",
            "Satisfactory but not outstanding.",
            "Decent product with some flaws."
        ],
        3.0: [
            "Average product. Nothing special but functional.",
            "Mediocre quality. Expected better for the price.",
            "Okay product with some issues. Not great.",
            "Average performance. Could be improved.",
            "Decent but not impressive. Basic functionality.",
            "Fair quality with some problems.",
            "Acceptable but not recommended.",
            "Average product with limitations.",
            "Basic functionality. Nothing exceptional.",
            "Mediocre quality. Expected more."
        ],
        2.5: [
            "Below average quality. Some issues with the product.",
            "Disappointing product with several problems.",
            "Poor quality for the price. Not recommended.",
            "Subpar product with multiple issues.",
            "Below expectations. Many problems.",
            "Poor performance and quality issues.",
            "Disappointing purchase. Would not recommend.",
            "Low quality product with defects.",
            "Unsatisfactory product with problems.",
            "Poor value for money. Many issues."
        ],
        2.0: [
            "Poor quality product. Many issues and problems.",
            "Disappointing purchase. Quality is very low.",
            "Bad product with multiple defects.",
            "Poor performance and quality. Not recommended.",
            "Low quality product with many problems.",
            "Unsatisfactory purchase. Many issues.",
            "Poor product with defects and problems.",
            "Bad quality for the price. Disappointing.",
            "Low quality product. Would not buy again.",
            "Poor purchase with many problems."
        ],
        1.5: [
            "Very poor quality. Many defects and issues.",
            "Terrible product with multiple problems.",
            "Extremely disappointing purchase.",
            "Very bad quality. Many defects.",
            "Poor product with serious issues.",
            "Terrible quality for the price.",
            "Very disappointing purchase.",
            "Bad product with many problems.",
            "Extremely poor quality.",
            "Terrible purchase experience."
        ],
        1.0: [
            "Worst product ever. Complete waste of money.",
            "Terrible quality with many defects.",
            "Extremely poor product. Do not buy!",
            "Worst purchase experience ever.",
            "Completely defective product.",
            "Terrible quality and service.",
            "Worst product I've ever bought.",
            "Complete disappointment. Avoid this product.",
            "Extremely bad quality. Waste of money.",
            "Terrible product with no redeeming qualities."
        ]
    }
    
    reviews = []
    
    # Create reviews for 60% of products (to simulate realistic review distribution)
    products_to_review = random.sample(products, int(len(products) * 0.6))
    
    for product in products_to_review:
        # Generate 1-5 reviews per product
        num_reviews = random.randint(1, 5)
        reviewers = random.sample(buyers, min(num_reviews, len(buyers)))
        
        for buyer in reviewers:
            # Generate rating (weighted towards positive ratings)
            rating_weights = {
                5.0: 0.25,  # 25% chance
                4.5: 0.20,  # 20% chance
                4.0: 0.20,  # 20% chance
                3.5: 0.15,  # 15% chance
                3.0: 0.10,  # 10% chance
                2.5: 0.05,  # 5% chance
                2.0: 0.03,  # 3% chance
                1.5: 0.01,  # 1% chance
                1.0: 0.01   # 1% chance
            }
            
            rating = random.choices(list(rating_weights.keys()), weights=list(rating_weights.values()))[0]
            
            # Get appropriate review template
            templates = review_templates.get(rating, review_templates[4.0])
            comment = random.choice(templates)
            
            # Add some product-specific details
            if product.category.name in ['Electronics', 'Computer and Tech']:
                comment += " Great for tech enthusiasts!"
            elif product.category.name in ['Clothes and Wear']:
                comment += " Perfect fit and comfortable material."
            elif product.category.name in ['Home Interiors']:
                comment += " Beautiful design and sturdy construction."
            elif product.category.name in ['Sports and Outdoor']:
                comment += " Durable and perfect for outdoor activities."
            
            # Create review
            review = ProductReview.objects.create(
                buyer=buyer,
                product=product,
                rating=rating,
                comment=comment
            )
            
            reviews.append(review)
            print(f"✓ Created {rating}-star review for {product.name} by {buyer.name}")
    
    return reviews

def create_seller_reviews():
    """Create seller reviews from buyers"""
    print("\nCreating Seller Reviews...")
    
    buyers = list(Buyer.objects.all())
    sellers = list(Seller.objects.all())
    
    if not buyers:
        print("❌ No buyers found. Please run buyer population script first.")
        return []
    
    if not sellers:
        print("❌ No sellers found. Please run seller population script first.")
        return []
    
    # Seller review templates
    seller_review_templates = {
        5.0: [
            "Excellent seller! Very professional and reliable.",
            "Outstanding service and communication. Highly recommend!",
            "Great seller with excellent products and fast shipping.",
            "Amazing experience! Professional and trustworthy seller.",
            "Outstanding quality and customer service. 5 stars!",
            "Excellent seller with great products and service.",
            "Fantastic experience! Highly professional and reliable.",
            "Outstanding seller with excellent communication.",
            "Great service and quality products. Highly satisfied!",
            "Excellent seller with fast delivery and great products."
        ],
        4.5: [
            "Very good seller with quality products.",
            "Great service and good communication.",
            "Good seller with reliable products.",
            "Professional seller with good service.",
            "Satisfactory experience with quality products.",
            "Good seller with reasonable prices.",
            "Reliable seller with good products.",
            "Professional service and good quality.",
            "Good experience with this seller.",
            "Quality products and good service."
        ],
        4.0: [
            "Good seller with acceptable service.",
            "Decent seller with reasonable quality.",
            "Acceptable service and products.",
            "Fair seller with adequate service.",
            "Good enough seller for the price.",
            "Satisfactory seller with standard service.",
            "Decent seller with acceptable quality.",
            "Reasonable seller with fair service.",
            "Good basic service and products.",
            "Acceptable seller with adequate quality."
        ],
        3.5: [
            "Average seller with some issues.",
            "Mediocre service but functional.",
            "Okay seller with minor problems.",
            "Average service with room for improvement.",
            "Decent seller with some limitations.",
            "Fair service with minor issues.",
            "Acceptable seller with some problems.",
            "Average seller with limitations.",
            "Basic service. Could be improved.",
            "Mediocre seller with some flaws."
        ],
        3.0: [
            "Average seller. Nothing special.",
            "Mediocre service. Expected better.",
            "Okay seller with some issues.",
            "Average service. Could be improved.",
            "Decent but not impressive seller.",
            "Fair service with some problems.",
            "Acceptable but not recommended.",
            "Average seller with limitations.",
            "Basic service. Nothing exceptional.",
            "Mediocre seller. Expected more."
        ],
        2.5: [
            "Below average seller with issues.",
            "Disappointing service and products.",
            "Poor seller with multiple problems.",
            "Subpar service with quality issues.",
            "Below expectations. Many problems.",
            "Poor service and communication.",
            "Disappointing seller. Would not recommend.",
            "Low quality service with problems.",
            "Unsatisfactory seller with issues.",
            "Poor value for money. Many problems."
        ],
        2.0: [
            "Poor seller with many issues.",
            "Disappointing service. Quality is low.",
            "Bad seller with multiple problems.",
            "Poor service and communication.",
            "Low quality seller with many problems.",
            "Unsatisfactory service. Many issues.",
            "Poor seller with defects and problems.",
            "Bad service for the price. Disappointing.",
            "Low quality seller. Would not buy again.",
            "Poor seller with many problems."
        ],
        1.5: [
            "Very poor seller with many issues.",
            "Terrible service with multiple problems.",
            "Extremely disappointing seller.",
            "Very bad service. Many problems.",
            "Poor seller with serious issues.",
            "Terrible service for the price.",
            "Very disappointing seller.",
            "Bad seller with many problems.",
            "Extremely poor service.",
            "Terrible seller experience."
        ],
        1.0: [
            "Worst seller ever. Avoid at all costs!",
            "Terrible service with many problems.",
            "Extremely poor seller. Do not buy!",
            "Worst seller experience ever.",
            "Completely unreliable seller.",
            "Terrible service and communication.",
            "Worst seller I've ever dealt with.",
            "Complete disappointment. Avoid this seller.",
            "Extremely bad service. Waste of money.",
            "Terrible seller with no redeeming qualities."
        ]
    }
    
    reviews = []
    
    # Create reviews for 70% of sellers (to simulate realistic review distribution)
    sellers_to_review = random.sample(sellers, int(len(sellers) * 0.7))
    
    for seller in sellers_to_review:
        # Generate 1-8 reviews per seller
        num_reviews = random.randint(1, 8)
        reviewers = random.sample(buyers, min(num_reviews, len(buyers)))
        
        for buyer in reviewers:
            # Generate rating (weighted towards positive ratings)
            rating_weights = {
                5.0: 0.30,  # 30% chance
                4.5: 0.25,  # 25% chance
                4.0: 0.20,  # 20% chance
                3.5: 0.12,  # 12% chance
                3.0: 0.08,  # 8% chance
                2.5: 0.03,  # 3% chance
                2.0: 0.01,  # 1% chance
                1.5: 0.005, # 0.5% chance
                1.0: 0.005  # 0.5% chance
            }
            
            rating = random.choices(list(rating_weights.keys()), weights=list(rating_weights.values()))[0]
            
            # Get appropriate review template
            templates = seller_review_templates.get(rating, seller_review_templates[4.0])
            comment = random.choice(templates)
            
            # Add some seller-specific details
            if seller.shop_name:
                comment += f" {seller.shop_name} is a reliable seller."
            
            # Create review
            review = SellerReview.objects.create(
                buyer=buyer,
                seller=seller,
                rating=rating,
                comment=comment
            )
            
            reviews.append(review)
            print(f"✓ Created {rating}-star review for {seller.shop_name} by {buyer.name}")
    
    return reviews

def create_review_likes():
    """Create likes/dislikes for reviews"""
    print("\nCreating Review Likes/Dislikes...")
    
    buyers = list(Buyer.objects.all())
    product_reviews = list(ProductReview.objects.all())
    seller_reviews = list(SellerReview.objects.all())
    
    likes_created = 0
    
    # Create likes for product reviews
    for review in product_reviews:
        # 20-60% of buyers will like/dislike this review
        num_interactions = random.randint(int(len(buyers) * 0.2), int(len(buyers) * 0.6))
        interacting_buyers = random.sample(buyers, min(num_interactions, len(buyers)))
        
        for buyer in interacting_buyers:
            # 80% chance of like, 20% chance of dislike
            is_like = random.choices([True, False], weights=[0.8, 0.2])[0]
            
            like, created = ProductReviewLike.objects.get_or_create(
                buyer=buyer,
                review=review,
                defaults={'is_like': is_like}
            )
            
            if created:
                likes_created += 1
                action = "liked" if is_like else "disliked"
                print(f"✓ {buyer.name} {action} review for {review.product.name}")
    
    # Create likes for seller reviews
    for review in seller_reviews:
        # 20-60% of buyers will like/dislike this review
        num_interactions = random.randint(int(len(buyers) * 0.2), int(len(buyers) * 0.6))
        interacting_buyers = random.sample(buyers, min(num_interactions, len(buyers)))
        
        for buyer in interacting_buyers:
            # 80% chance of like, 20% chance of dislike
            is_like = random.choices([True, False], weights=[0.8, 0.2])[0]
            
            like, created = SellerReviewLike.objects.get_or_create(
                buyer=buyer,
                review=review,
                defaults={'is_like': is_like}
            )
            
            if created:
                likes_created += 1
                action = "liked" if is_like else "disliked"
                print(f"✓ {buyer.name} {action} review for {review.seller.shop_name}")
    
    return likes_created

def update_rating_averages():
    """Update rating averages for products and sellers"""
    print("\nUpdating Rating Averages...")
    
    # Update product rating averages
    for product in Product.objects.all():
        product.update_rating_avg()
        if product.rating_avg:
            print(f"✓ Updated {product.name} rating: {product.rating_avg:.1f}")
    
    # Update seller rating averages
    for seller in Seller.objects.all():
        seller.update_rating_avg()
        if seller.rating:
            print(f"✓ Updated {seller.shop_name} rating: {seller.rating:.1f}")

def validate_review_data():
    """Validate that all review data is properly created"""
    print("\n🔍 Validating Review Data...")
    
    # Check product reviews
    product_reviews = ProductReview.objects.count()
    print(f"✓ Product Reviews: {product_reviews}")
    
    # Check seller reviews
    seller_reviews = SellerReview.objects.count()
    print(f"✓ Seller Reviews: {seller_reviews}")
    
    # Check review likes
    product_likes = ProductReviewLike.objects.count()
    seller_likes = SellerReviewLike.objects.count()
    total_likes = product_likes + seller_likes
    print(f"✓ Review Likes/Dislikes: {total_likes} (Product: {product_likes}, Seller: {seller_likes})")
    
    # Check rating distribution for products
    print(f"\n📊 Product Review Rating Distribution:")
    for rating in [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0]:
        count = ProductReview.objects.filter(rating=rating).count()
        if count > 0:
            percentage = (count / product_reviews) * 100
            print(f"   • {rating} stars: {count} reviews ({percentage:.1f}%)")
    
    # Check rating distribution for sellers
    print(f"\n📊 Seller Review Rating Distribution:")
    for rating in [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0]:
        count = SellerReview.objects.filter(rating=rating).count()
        if count > 0:
            percentage = (count / seller_reviews) * 100
            print(f"   • {rating} stars: {count} reviews ({percentage:.1f}%)")
    
    # Check products with updated ratings
    products_with_ratings = Product.objects.filter(rating_avg__isnull=False).count()
    sellers_with_ratings = Seller.objects.filter(rating__isnull=False).count()
    print(f"\n📈 Updated Ratings:")
    print(f"   • Products with ratings: {products_with_ratings}")
    print(f"   • Sellers with ratings: {sellers_with_ratings}")
    
    # Check average ratings
    if products_with_ratings > 0:
        avg_product_rating = sum(p.rating_avg for p in Product.objects.filter(rating_avg__isnull=False)) / products_with_ratings
        print(f"   • Average product rating: {avg_product_rating:.2f}")
    
    if sellers_with_ratings > 0:
        avg_seller_rating = sum(s.rating for s in Seller.objects.filter(rating__isnull=False)) / sellers_with_ratings
        print(f"   • Average seller rating: {avg_seller_rating:.2f}")

def main():
    """Main function to populate reviews"""
    print("Starting to populate Product Reviews and Seller Reviews...")
    print("=" * 70)
    
    # Check prerequisites
    if not Buyer.objects.exists():
        print("❌ No buyers found. Please run buyer population script first.")
        return
    
    if not Seller.objects.exists():
        print("❌ No sellers found. Please run seller population script first.")
        return
    
    if not Product.objects.exists():
        print("❌ No products found. Please run seller and product population script first.")
        return
    
    # Create product reviews
    product_reviews = create_product_reviews()
    
    # Create seller reviews
    seller_reviews = create_seller_reviews()
    
    # Create review likes/dislikes
    review_likes = create_review_likes()
    
    # Update rating averages
    update_rating_averages()
    
    # Validate data integrity
    validate_review_data()
    
    print("\n" + "=" * 70)
    print("✅ Product Reviews and Seller Reviews populated successfully!")
    print("=" * 70)
    
    # Print final summary
    print("\n📈 Final Summary:")
    print(f"   • Product Reviews: {ProductReview.objects.count()}")
    print(f"   • Seller Reviews: {SellerReview.objects.count()}")
    print(f"   • Review Likes/Dislikes: {ProductReviewLike.objects.count() + SellerReviewLike.objects.count()}")
    
    # Print sample data
    print("\n📝 Sample Product Reviews:")
    for review in ProductReview.objects.all()[:5]:
        print(f"   • {review.buyer.name} gave {review.product.name} {review.rating} stars")
    
    print("\n💼 Sample Seller Reviews:")
    for review in SellerReview.objects.all()[:5]:
        print(f"   • {review.buyer.name} gave {review.seller.shop_name} {review.rating} stars")
    
    print("\n⭐ Top Rated Products:")
    top_products = Product.objects.filter(rating_avg__isnull=False).order_by('-rating_avg')[:5]
    for product in top_products:
        print(f"   • {product.name}: {product.rating_avg:.1f} stars")
    
    print("\n🏆 Top Rated Sellers:")
    top_sellers = Seller.objects.filter(rating__isnull=False).order_by('-rating')[:5]
    for seller in top_sellers:
        print(f"   • {seller.shop_name}: {seller.rating:.1f} stars")

if __name__ == "__main__":
    main() 