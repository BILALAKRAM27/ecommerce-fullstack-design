# Seller and Product Population Script

This script populates the MarketVibe database with 20 seller accounts and 100 products (5 products per seller).

## File

- `populate_sellers_and_products.py` - Populates sellers and products

## Prerequisites

**IMPORTANT**: You must run the category and brand population scripts first:

1. **Categories**: Run `populate_categories.py` and `populate_categories_part2.py`
2. **Brands**: Run `populate_brands.py`
3. **Then**: Run this seller and product script

## How to Run

### Prerequisites
- Make sure you have Django set up and the database is migrated
- Ensure you're in the Django project root directory (where `manage.py` is located)
- **Must run category and brand population scripts first**

### Running the Script

```bash
python populate_sellers_and_products.py
```

## What the Script Creates

### 👥 **20 Seller Accounts**

**User Accounts:**
- Username: seller1, seller2, ..., seller20
- Email: seller1@gmail.com, seller2@gmail.com, ..., seller20@gmail.com
- Password: "marketvibe27" (for all accounts)

**Seller Profiles:**
- **Shop Names**: Tech Haven, Digital Dreams, Smart Solutions, Gadget Galaxy, Tech Trends, etc.
- **Shop Descriptions**: Unique descriptions for each shop
- **Addresses**: Shop addresses with unique numbers
- **Ratings**: Random ratings between 3.5 and 5.0

### 🛍️ **100 Products (5 per seller)**

Each seller gets 5 unique products with:

- **Realistic Names**: Brand + Product Type (e.g., "Samsung Premium Smartphone")
- **Appropriate Prices**: Based on product category and type
- **Stock Levels**: Realistic inventory quantities
- **Categories**: Randomly assigned from existing categories
- **Brands**: Randomly assigned from existing brands
- **Conditions**: New, Used, or Refurbished
- **Discounts**: 30% chance of having 5-20% discount

## Product Categories Covered

The script creates products across all major categories:

### 📦 **Electronics**
- Smartphones ($299-$899)
- Laptops ($599-$1499)
- Smart Watches ($199-$599)
- LED TVs ($399-$1999)
- Bluetooth Speakers ($49-$299)
- Cameras ($199-$2499)
- Headphones ($89-$399)
- Power Banks ($49-$149)
- Gaming Consoles ($199-$699)
- Drones ($99-$1299)

### 🚗 **Automobiles**
- Cars ($18,000-$50,000)
- Bikes ($8,000-$20,000)
- Electric Scooters ($799-$1999)
- Car Accessories ($19-$89)
- Tyres ($179-$299)
- Car Batteries ($149-$299)
- Motorbike Helmets ($129-$299)
- Car Audio Systems ($199-$599)
- Truck Parts ($299-$899)
- SUV Accessories ($89-$299)

### 👕 **Clothing**
- Men's T-Shirts ($24-$39)
- Women's Dresses ($49-$89)
- Men's Jeans ($69-$84)
- Women's Tops ($24-$54)
- Children's Clothing ($19-$49)
- Footwear ($49-$119)
- Winter Jackets ($89-$199)
- Socks ($8-$14)
- Caps and Hats ($18-$34)
- Belts ($29-$49)

## Features

- **Realistic Data**: Products have appropriate names, prices, and descriptions
- **Category Matching**: Products are assigned to relevant categories
- **Brand Integration**: Products use existing brands from the database
- **Price Variation**: Realistic pricing based on product type and category
- **Stock Management**: Appropriate stock levels for different product types
- **Discount System**: Some products have random discounts
- **Condition Variety**: Products can be New, Used, or Refurbished
- **Error Handling**: Graceful handling of missing data
- **Progress Tracking**: Real-time progress updates
- **Summary Report**: Complete database statistics

## Database Models Used

- `User`: Django user accounts
- `Seller`: Seller profiles with shop information
- `Product`: Product listings with all details
- `Category`: Product categories (from previous scripts)
- `Brand`: Product brands (from previous scripts)

## Expected Output

```
Starting to populate database with sellers and products...
============================================================
✓ Created user: seller1
✓ Created seller: Tech Haven
✓ Created user: seller2
✓ Created seller: Digital Dreams
...

✅ Successfully created 20 seller accounts
============================================================

Creating products for Tech Haven...
  ✓ Created: Samsung Premium Smartphone - $599.99
  ✓ Created: Apple Gaming Laptop - $1299.99
  ✓ Created: JBL Wireless Headphones - $199.99
  ✓ Created: Canon DSLR Camera - $899.99
  ✓ Created: Anker High Capacity Power Bank - $79.99

Creating products for Digital Dreams...
  ✓ Created: HP Business Laptop - $899.99
  ✓ Created: Sony 4K Smart TV - $799.99
  ✓ Created: Bose Noise Cancelling - $299.99
  ✓ Created: Nikon Mirrorless Camera - $1099.99
  ✓ Created: Xiaomi Fast Charging Power Bank - $99.99
...

============================================================
✅ Successfully created 20 seller accounts
✅ Successfully created 100 products
📊 Average products per seller: 5.0
============================================================

📈 Database Summary:
   • Total Users: 20
   • Total Sellers: 20
   • Total Products: 100
   • Total Categories: 90
   • Total Brands: 270

🛍️ Sample Products Created:
   • Samsung Premium Smartphone - $599.99 (Tech Haven)
   • Apple Gaming Laptop - $1299.99 (Tech Haven)
   • JBL Wireless Headphones - $199.99 (Tech Haven)
   • Canon DSLR Camera - $899.99 (Tech Haven)
   • Anker High Capacity Power Bank - $79.99 (Tech Haven)
   • HP Business Laptop - $899.99 (Digital Dreams)
   • Sony 4K Smart TV - $799.99 (Digital Dreams)
   • Bose Noise Cancelling - $299.99 (Digital Dreams)
   • Nikon Mirrorless Camera - $1099.99 (Digital Dreams)
   • Xiaomi Fast Charging Power Bank - $99.99 (Digital Dreams)
```

## Verification

After running the script, you can verify the data was created by:

1. **Django Admin Interface**: Check Users, Sellers, and Products
2. **Django Shell**: Query the models directly
3. **Database**: Check the database tables

Example Django shell commands:
```python
from django.contrib.auth.models import User
from seller.models import Seller, Product

# Check users
User.objects.filter(username__startswith='seller').count()

# Check sellers
Seller.objects.count()

# Check products
Product.objects.count()

# Check products per seller
for seller in Seller.objects.all():
    print(f"{seller.shop_name}: {seller.products.count()} products")

# Check sample products
Product.objects.all()[:5].values_list('name', 'base_price', 'seller__shop_name')
```

## Login Information

All seller accounts can be logged into with:
- **Username**: seller1, seller2, ..., seller20
- **Password**: marketvibe27

## Notes

- Script uses `get_or_create()` to avoid duplicates
- If sellers/products already exist, they won't be recreated
- Script includes comprehensive error handling
- Products are randomly assigned to categories and brands
- All foreign key relationships are properly maintained
- Script is designed to be run multiple times safely

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

This will give you a fully populated MarketVibe database with:
- 9 main categories with 90 subcategories
- 270+ brands
- 20 seller accounts
- 100 products 