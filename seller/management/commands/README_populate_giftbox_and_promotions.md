# Gift Box Campaigns and Product Promotions Population Script

This script populates the MarketVibe database with gift box campaigns and product promotions using the existing sellers and products.

## File

- `populate_giftbox_and_promotions.py` - Populates gift box campaigns and product promotions

## Prerequisites

**IMPORTANT**: You must run the seller and product population scripts first:

1. **Categories**: Run `populate_categories.py` and `populate_categories_part2.py`
2. **Brands**: Run `populate_brands.py`
3. **Sellers and Products**: Run `populate_sellers_and_products.py`
4. **Then**: Run this gift box and promotion script

## How to Run

### Prerequisites
- Make sure you have Django set up and the database is migrated
- Ensure you're in the Django project root directory (where `manage.py` is located)
- **Must run seller and product population scripts first**

### Running the Script

```bash
python populate_giftbox_and_promotions.py
```

## What the Script Creates

### 🎁 **10 Gift Box Campaigns**

**Campaign Details:**
- **Summer Essentials** - $149.99
- **Festive Delights** - $199.99
- **Tech Lover's Bundle** - $299.99
- **Fitness Fanatic Pack** - $179.99
- **Home Comfort Collection** - $129.99
- **Outdoor Adventure Kit** - $249.99
- **Beauty & Wellness Set** - $159.99
- **Gaming Enthusiast Box** - $349.99
- **Professional Workspace** - $229.99
- **Family Fun Package** - $189.99

**Features:**
- Each campaign has a meaningful name and description
- Reasonable prices ranging from $129.99 to $349.99
- Active campaigns with 3-6 month validity periods
- All 20 sellers participate in at least one campaign
- Some sellers participate in multiple campaigns for variety

### 📢 **5 Product Promotions**

**Promotion Types:**
1. **Flash Sale - Electronics** (25% off, min $100 order)
2. **Buy One Get One - Clothing** (50% off second item, min $50 order)
3. **Free Shipping Weekend** (Free shipping, min $75 order)
4. **Student Discount** (15% off, min $25 order, max $100 discount)
5. **Clearance Sale** (40% off, min $30 order, max $150 discount)

**Features:**
- Each promotion includes 2 products from the same seller
- Realistic discount percentages (10-40%)
- Minimum order amounts and maximum discount limits
- 30-90 day validity periods
- Usage limits (50-200 uses per promotion)

## Database Models Used

- `GiftBoxCampaign`: Campaign details with name, price, and dates
- `SellerGiftBoxParticipation`: Links sellers to campaigns
- `Promotion`: Product promotion details with discounts and rules
- `Seller`: Existing seller accounts
- `Product`: Existing products for promotion assignment

## Expected Output

```
Starting to populate Gift Box Campaigns and Product Promotions...
======================================================================
Creating Gift Box Campaigns...
✓ Created: Summer Essentials - $149.99
✓ Created: Festive Delights - $199.99
✓ Created: Tech Lover's Bundle - $299.99
✓ Created: Fitness Fanatic Pack - $179.99
✓ Created: Home Comfort Collection - $129.99
✓ Created: Outdoor Adventure Kit - $249.99
✓ Created: Beauty & Wellness Set - $159.99
✓ Created: Gaming Enthusiast Box - $349.99
✓ Created: Professional Workspace - $229.99
✓ Created: Family Fun Package - $189.99

Assigning sellers to campaigns...
✓ Tech Haven joined Summer Essentials
✓ Digital Dreams joined Festive Delights
✓ Smart Solutions joined Tech Lover's Bundle
...

📊 Total campaign participations: 35

Creating Product Promotions...
✓ Created: Flash Sale - Electronics by Tech Haven
  Products: Samsung Premium Smartphone, Apple Gaming Laptop
  Discount: 25.0% (min order: $100.0)
✓ Created: Buy One Get One - Clothing by Digital Dreams
  Products: Nike Cotton T-Shirt, Adidas Polo T-Shirt
  Discount: 50.0% (min order: $50.0)
...

🔍 Validating Data Integrity...
✓ Gift Box Campaigns: 10
✓ Seller Participations: 35
✓ Sellers in campaigns: 20/20
✓ Product Promotions: 5
✓ Promotions with products: 5

📋 Detailed Validation:
   • Summer Essentials: 4 sellers, $149.99
   • Festive Delights: 3 sellers, $199.99
   • Tech Lover's Bundle: 5 sellers, $299.99
   • Flash Sale - Electronics (Tech Haven): 2 products, 25.0% off
   • Buy One Get One - Clothing (Digital Dreams): 2 products, 50.0% off
...

======================================================================
✅ Gift Box Campaigns and Promotions populated successfully!
======================================================================

📈 Final Summary:
   • Gift Box Campaigns: 10
   • Seller Participations: 35
   • Product Promotions: 5
   • Total Sellers: 20
   • Total Products: 100

🎁 Sample Gift Box Campaigns:
   • Summer Essentials - $149.99 (4 sellers)
   • Festive Delights - $199.99 (3 sellers)
   • Tech Lover's Bundle - $299.99 (5 sellers)
   • Fitness Fanatic Pack - $179.99 (2 sellers)
   • Home Comfort Collection - $129.99 (3 sellers)

📢 Sample Product Promotions:
   • Flash Sale - Electronics - 25.0% off (2 products)
   • Buy One Get One - Clothing - 50.0% off (2 products)
   • Free Shipping Weekend - 0.0% off (2 products)
   • Student Discount - 15.0% off (2 products)
   • Clearance Sale - 40.0% off (2 products)
```

## Data Integrity Validation

The script includes comprehensive validation to ensure:

### ✅ **Gift Box Campaigns**
- All 20 sellers participate in at least one campaign
- Campaigns have valid start and end dates
- Prices are reasonable and realistic
- No duplicate campaign names

### ✅ **Product Promotions**
- Each promotion includes exactly 2 products from the same seller
- Products exist in the database
- Discount percentages are realistic (10-40%)
- Minimum order amounts are appropriate
- Maximum discount limits are set where applicable

### ✅ **Foreign Key Relationships**
- All seller-campaign relationships are properly maintained
- All seller-promotion relationships are valid
- All product-promotion relationships are valid
- No orphaned records

## Verification

After running the script, you can verify the data was created by:

1. **Django Admin Interface**: Check GiftBoxCampaign, SellerGiftBoxParticipation, and Promotion models
2. **Django Shell**: Query the models directly
3. **Database**: Check the database tables

Example Django shell commands:
```python
from seller.models import GiftBoxCampaign, SellerGiftBoxParticipation, Promotion

# Check gift box campaigns
GiftBoxCampaign.objects.count()
GiftBoxCampaign.objects.all().values_list('name', 'price')

# Check seller participations
SellerGiftBoxParticipation.objects.count()
for campaign in GiftBoxCampaign.objects.all():
    print(f"{campaign.name}: {campaign.participants.count()} sellers")

# Check promotions
Promotion.objects.count()
for promotion in Promotion.objects.all():
    print(f"{promotion.name}: {promotion.products.count()} products, {promotion.discount_value}% off")

# Check seller participation distribution
for seller in Seller.objects.all():
    campaigns = seller.giftbox_participations.count()
    promotions = seller.promotions.count()
    print(f"{seller.shop_name}: {campaigns} campaigns, {promotions} promotions")
```

## Features

- **Realistic Campaign Names**: Meaningful names like "Summer Essentials", "Tech Lover's Bundle"
- **Appropriate Pricing**: Campaign prices range from $129.99 to $349.99
- **Seller Distribution**: All sellers participate in at least one campaign
- **Variety**: Some sellers participate in multiple campaigns
- **Product Promotions**: 5 distinct promotion types with realistic discounts
- **Data Validation**: Comprehensive integrity checks
- **Error Handling**: Graceful handling of missing data
- **Progress Tracking**: Real-time progress updates
- **Summary Reports**: Complete database statistics

## Notes

- Script uses `get_or_create()` to avoid duplicates
- If campaigns/promotions already exist, they won't be recreated
- Script includes comprehensive error handling and validation
- All foreign key relationships are properly maintained
- Script is designed to be run multiple times safely
- Campaigns have 3-6 month validity periods
- Promotions have 30-90 day validity periods

## Complete Setup Process

1. **Run category scripts:**
   ```bash
   python populate_categories.py
   python populate_categories_part2.py
   ```

2. **Run brand script:**
   ```bash
   python populate_brands.py
   ```

3. **Run seller and product script:**
   ```bash
   python populate_sellers_and_products.py
   ```

4. **Run gift box and promotion script:**
   ```bash
   python populate_giftbox_and_promotions.py
   ```

This will give you a fully populated MarketVibe database with:
- 9 main categories with 90 subcategories
- 270+ brands
- 20 seller accounts
- 100 products
- 10 gift box campaigns
- 35+ seller campaign participations
- 5 product promotions 