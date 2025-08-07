# Review Population Script

This script populates the MarketVibe database with realistic product reviews and seller reviews from buyers.

## 📋 What This Script Does

### Product Reviews
- Creates reviews for 60% of products (realistic distribution)
- Generates 1-5 reviews per product
- Uses weighted rating distribution (biased towards positive ratings)
- Includes category-specific review comments
- Creates review likes/dislikes

### Seller Reviews
- Creates reviews for 70% of sellers (realistic distribution)
- Generates 1-8 reviews per seller
- Uses weighted rating distribution (biased towards positive ratings)
- Includes seller-specific review comments
- Creates review likes/dislikes

### Rating Averages
- Updates product rating averages automatically
- Updates seller rating averages automatically
- Provides comprehensive validation and statistics

## 🚀 Prerequisites

Before running this script, ensure you have:

1. **Buyers**: Run `populate_buyers_and_orders.py` first
2. **Sellers**: Run `populate_sellers_and_products.py` first
3. **Products**: Products should be created with the seller population script

## 📝 Usage

```bash
python populate_reviews.py
```

## 🎯 Features

### Product Review Features
- **Realistic Rating Distribution**: Weighted towards positive ratings (4-5 stars)
- **Category-Specific Comments**: Different comments for Electronics, Clothing, Home Interiors, Sports, etc.
- **Multiple Review Templates**: 10 different templates per rating level
- **Review Likes/Dislikes**: 20-60% of buyers interact with each review
- **Automatic Rating Updates**: Updates product `rating_avg` field

### Seller Review Features
- **Professional Review Templates**: Service-focused comments
- **Weighted Rating Distribution**: 30% 5-star, 25% 4.5-star, etc.
- **Seller-Specific Comments**: Includes shop name in comments
- **Review Interaction**: Likes/dislikes for seller reviews
- **Automatic Rating Updates**: Updates seller `rating` field

### Data Integrity Features
- **Prerequisite Validation**: Checks for required data before running
- **Realistic Relationships**: Links to existing buyers, sellers, and products
- **Unique Constraints**: Respects unique buyer-product and buyer-seller relationships
- **Comprehensive Validation**: Detailed reporting of created data

## 📊 Expected Output

### Product Reviews Created
- **~60 Product Reviews** (60% of products reviewed)
- **Realistic rating distribution**: 25% 5-star, 20% 4.5-star, 20% 4-star, etc.
- **Category-specific comments** with product details
- **Review interactions** with likes/dislikes

### Seller Reviews Created
- **~14 Seller Reviews** (70% of sellers reviewed)
- **Service-focused comments** about professionalism and reliability
- **Weighted rating distribution** with more positive ratings
- **Review interactions** with likes/dislikes

### Rating Averages Updated
- **Product rating averages** calculated and stored
- **Seller rating averages** calculated and stored
- **Top-rated products and sellers** identified

### Validation Report
- Review counts and distributions
- Rating distribution analysis
- Average ratings calculation
- Top-rated items summary

## 🔍 Verification

After running the script, you can verify the data:

### Check Product Reviews
```python
from seller.models import ProductReview
ProductReview.objects.count()  # Should be ~60
```

### Check Seller Reviews
```python
from seller.models import SellerReview
SellerReview.objects.count()  # Should be ~14
```

### Check Review Likes
```python
from seller.models import ProductReviewLike, SellerReviewLike
ProductReviewLike.objects.count()  # Should be significant
SellerReviewLike.objects.count()   # Should be significant
```

### Check Rating Averages
```python
from seller.models import Product, Seller
Product.objects.filter(rating_avg__isnull=False).count()  # Should be ~60
Seller.objects.filter(rating__isnull=False).count()      # Should be ~14
```

## 📈 Sample Data Created

### Product Review Examples
- **5-star**: "Excellent product! Exceeded my expectations. Highly recommend!"
- **4.5-star**: "Very good product with minor improvements possible."
- **4-star**: "Good product overall. Meets basic expectations."
- **3.5-star**: "Average product with some issues. Could be better."
- **Category-specific**: "Great for tech enthusiasts!" (Electronics)

### Seller Review Examples
- **5-star**: "Excellent seller! Very professional and reliable."
- **4.5-star**: "Very good seller with quality products."
- **4-star**: "Good seller with acceptable service."
- **Service-focused**: Comments about communication, shipping, quality

### Rating Distribution
- **Product Reviews**: 25% 5-star, 20% 4.5-star, 20% 4-star, 15% 3.5-star, etc.
- **Seller Reviews**: 30% 5-star, 25% 4.5-star, 20% 4-star, 12% 3.5-star, etc.

## 🛠️ Technical Details

### Models Used
- `ProductReview`: Buyer reviews for products with ratings and comments
- `SellerReview`: Buyer reviews for sellers with ratings and comments
- `ProductReviewLike`: Likes/dislikes for product reviews
- `SellerReviewLike`: Likes/dislikes for seller reviews
- `Product`: Links to products being reviewed
- `Seller`: Links to sellers being reviewed
- `Buyer`: Links to buyers writing reviews

### Key Features
- **Weighted Rating Generation**: Realistic distribution with positive bias
- **Template-Based Comments**: Pre-written templates for different rating levels
- **Category-Specific Details**: Different comments for different product categories
- **Automatic Rating Updates**: Calls `update_rating_avg()` methods
- **Review Interaction**: Creates likes/dislikes for social engagement

## ✅ Success Indicators

The script runs successfully when you see:
- ✅ All prerequisite checks pass
- ✅ Product reviews created with realistic ratings
- ✅ Seller reviews created with service-focused comments
- ✅ Review likes/dislikes generated
- ✅ Rating averages updated
- ✅ Validation report shows expected distributions
- ✅ Final summary displays top-rated items

## 🔧 Troubleshooting

### Common Issues
1. **"No buyers found"**: Run buyer population script first
2. **"No sellers found"**: Run seller population script first
3. **"No products found"**: Run seller and product population script first
4. **Import errors**: Ensure Django environment is properly set up

### Data Verification
- Check that reviews link to existing buyers, sellers, and products
- Verify that rating averages are calculated correctly
- Confirm that review likes/dislikes are created
- Ensure unique constraints are respected

## 📚 Related Scripts

This script is part of the complete MarketVibe database population suite:

1. `populate_categories.py` - Product categories and attributes
2. `populate_categories_part2.py` - Additional categories
3. `populate_brands.py` - Product brands
4. `populate_sellers_and_products.py` - Seller accounts and products
5. `populate_giftbox_and_promotions.py` - Gift box campaigns and promotions
6. `populate_product_attributes.py` - Product attribute values
7. `populate_buyers_and_orders.py` - Buyer accounts and orders
8. `populate_quotes.py` - Quote requests and responses
9. **`populate_reviews.py`** - Product and seller reviews (this script)

## 🎉 Complete Setup

To populate the entire MarketVibe database:

```bash
# 1. Categories and attributes
python populate_categories.py
python populate_categories_part2.py

# 2. Brands
python populate_brands.py

# 3. Sellers and products
python populate_sellers_and_products.py

# 4. Gift boxes and promotions
python populate_giftbox_and_promotions.py

# 5. Product attributes
python populate_product_attributes.py

# 6. Buyers and orders
python populate_buyers_and_orders.py

# 7. Quotes
python populate_quotes.py

# 8. Reviews (this script)
python populate_reviews.py
```

This will create a fully populated MarketVibe database with realistic test data for all major features including comprehensive review systems! 