# Buyer Accounts and Orders Population Script

This script populates the MarketVibe database with 20 buyer accounts and 100 orders (5 orders per buyer) with a mix of regular products, promotions, and gift boxes.

## File

- `populate_buyers_and_orders.py` - Populates buyer accounts and orders

## Prerequisites

**IMPORTANT**: You must run all the previous population scripts first:

1. **Categories**: Run `populate_categories.py` and `populate_categories_part2.py`
2. **Brands**: Run `populate_brands.py`
3. **Sellers and Products**: Run `populate_sellers_and_products.py`
4. **Gift Box and Promotions**: Run `populate_giftbox_and_promotions.py`
5. **Product Attributes**: Run `populate_product_attributes.py`
6. **Then**: Run this buyer and order script

## How to Run

### Prerequisites
- Make sure you have Django set up and the database is migrated
- Ensure you're in the Django project root directory (where `manage.py` is located)
- **Must run all previous population scripts first**

### Running the Script

```bash
python populate_buyers_and_orders.py
```

## What the Script Creates

### 👤 **20 Buyer Accounts**

**User Accounts:**
- Username: buyer1, buyer2, ..., buyer20
- Email: buyer1@gmail.com, buyer2@gmail.com, ..., buyer20@gmail.com
- Password: "marketvibe27" (for all accounts)

**Buyer Profiles:**
- **Names**: John Smith, Sarah Johnson, Michael Brown, Emily Davis, David Wilson, etc.
- **Phone Numbers**: Realistic US phone numbers
- **Addresses**: Complete addresses with street, city, zip code, country
- **Detailed Addresses**: Separate Address model entries for each buyer

### 📦 **100 Orders (5 per buyer)**

Each buyer gets 5 orders with the following distribution:

#### **Regular Product Orders (2 per buyer)**
- **Products**: 1-3 random products from the same seller
- **Quantities**: 1-3 units per product
- **Pricing**: Uses product's calculated final price
- **Status**: Random (pending, processing, shipped, delivered)
- **Payment**: Cash on Delivery (COD)
- **Delivery**: 3-14 days expected delivery

#### **Promotion Orders (2 per buyer)**
- **Products**: 1-2 products from a promotion
- **Promotions**: Random selection from existing promotions
- **Discounts**: Applied based on promotion type and rules
- **Status**: Random (pending, processing, shipped)
- **Payment**: Cash on Delivery (COD)
- **Notes**: Includes promotion name in order notes

#### **Gift Box Orders (1 per buyer)**
- **Campaigns**: Random gift box campaign selection
- **Sellers**: Sellers participating in the selected campaign
- **Products**: 0-3 additional products from the seller
- **Messages**: Random gift messages (Happy Birthday, Congratulations, etc.)
- **Status**: Random (pending, packed, shipped)
- **Payment**: Cash on Delivery (COD)
- **Reveal Contents**: Random boolean (true/false)

### 🔔 **Buyer Notifications**

Each buyer gets 1-3 notifications:
- **Order Updates**: Shipping notifications
- **Price Drop Alerts**: Wishlist product price changes
- **Low Stock Alerts**: Recently viewed products
- **System Messages**: Welcome messages

## Database Models Used

- `User`: Django user accounts
- `Buyer`: Buyer profiles with personal information
- `Address`: Detailed buyer addresses
- `Order`: Regular product orders
- `OrderItem`: Individual items in orders
- `GiftBoxOrder`: Gift box orders
- `BuyerNotification`: Buyer notifications
- `Seller`: Existing seller accounts
- `Product`: Existing products
- `Promotion`: Existing promotions
- `GiftBoxCampaign`: Existing gift box campaigns

## Expected Output

```
Starting to populate Buyer Accounts and Orders...
======================================================================
Creating Buyer Accounts...
✓ Created user: buyer1
✓ Created buyer: John Smith (buyer1@gmail.com)
✓ Created user: buyer2
✓ Created buyer: Sarah Johnson (buyer2@gmail.com)
...

Creating Buyer Addresses...
✓ Created address for John Smith
✓ Created address for Sarah Johnson
...

Creating Regular Product Orders...
✓ Created regular order for John Smith: $299.99 (2 products)
✓ Created regular order for John Smith: $189.50 (3 products)
✓ Created regular order for Sarah Johnson: $450.75 (1 products)
...

Creating Promotion Orders...
✓ Created promotion order for John Smith: $89.99 (Promotion: Flash Sale - Electronics)
✓ Created promotion order for Sarah Johnson: $149.50 (Promotion: Student Discount)
...

Creating Gift Box Orders...
✓ Created gift box order for John Smith: $349.99 (Campaign: Tech Lover's Bundle)
✓ Created gift box order for Sarah Johnson: $199.99 (Campaign: Summer Essentials)
...

Creating Buyer Notifications...
✓ Created notification for John Smith: Order Update
✓ Created notification for Sarah Johnson: Price Drop Alert
...

🔍 Validating Data Integrity...
✓ Buyer Accounts: 20
✓ Regular Orders: 40
✓ Gift Box Orders: 20
✓ Total Orders: 60
✓ Order Items: 120
✓ Buyer Addresses: 20
✓ Buyer Notifications: 45

📋 Detailed Validation:
   • John Smith: 4 regular orders, 1 gift box orders, 2 notifications
   • Sarah Johnson: 4 regular orders, 1 gift box orders, 3 notifications
   • Michael Brown: 4 regular orders, 1 gift box orders, 1 notifications
   • Orders with Promotions: 40
   • COD Orders: 40 regular + 20 gift box = 60

======================================================================
✅ Buyer Accounts and Orders populated successfully!
======================================================================

📈 Final Summary:
   • Buyer Accounts: 20
   • Regular Orders: 40
   • Gift Box Orders: 20
   • Order Items: 120
   • Buyer Addresses: 20
   • Buyer Notifications: 45

👤 Sample Buyer Accounts:
   • John Smith (buyer1@gmail.com): 4 orders, 1 gift boxes
   • Sarah Johnson (buyer2@gmail.com): 4 orders, 1 gift boxes
   • Michael Brown (buyer3@gmail.com): 4 orders, 1 gift boxes
   • Emily Davis (buyer4@gmail.com): 4 orders, 1 gift boxes
   • David Wilson (buyer5@gmail.com): 4 orders, 1 gift boxes

📦 Sample Orders:
   • ORD-000001: $299.99 (2 items) - pending
   • ORD-000002: $189.50 (3 items) - processing
   • ORD-000003: $450.75 (1 items) - shipped
   • ORD-000004: $89.99 (2 items) - delivered
   • ORD-000005: $149.50 (1 items) - pending

🎁 Sample Gift Box Orders:
   • GB-000001: $349.99 (3 products) - pending
   • GB-000002: $199.99 (2 products) - packed
   • GB-000003: $299.99 (1 products) - shipped
   • GB-000004: $249.99 (0 products) - pending
   • GB-000005: $179.99 (2 products) - packed
```

## Data Integrity Validation

The script includes comprehensive validation to ensure:

### ✅ **Buyer Account Creation**
- All 20 buyer accounts created with unique emails
- User accounts created with proper credentials
- Detailed addresses created for each buyer
- Realistic phone numbers and addresses

### ✅ **Order Creation**
- Each buyer gets exactly 5 orders (2 regular + 2 promotion + 1 gift box)
- All orders use Cash on Delivery (COD) payment method
- Proper foreign key relationships maintained
- Realistic pricing and quantities

### ✅ **Promotion Integration**
- Orders with promotions include the promotion reference
- Discounts are calculated correctly based on promotion rules
- Promotion products are properly linked

### ✅ **Gift Box Integration**
- Gift box orders link to existing campaigns
- Sellers participating in campaigns are used
- Additional products can be added to gift boxes
- Realistic gift messages included

### ✅ **Payment Method**
- All orders use 'cod' (Cash on Delivery) as specified
- Payment status set to 'pending' for COD orders
- Proper order type field values

### ✅ **Foreign Key Relationships**
- All buyer-order relationships are valid
- All order-seller relationships are valid
- All order-product relationships are valid
- All promotion relationships are valid
- All gift box campaign relationships are valid

## Verification

After running the script, you can verify the data was created by:

1. **Django Admin Interface**: Check Buyer, Order, GiftBoxOrder, and Address models
2. **Django Shell**: Query the models directly
3. **Database**: Check the database tables

Example Django shell commands:
```python
from buyer.models import Buyer, Order, GiftBoxOrder, Address
from seller.models import Seller, Product, Promotion

# Check buyers
Buyer.objects.count()
Buyer.objects.all().values_list('name', 'email')

# Check orders
Order.objects.count()
Order.objects.filter(order_type='cod').count()

# Check gift box orders
GiftBoxOrder.objects.count()
GiftBoxOrder.objects.filter(order_type='cod').count()

# Check orders with promotions
Order.objects.filter(promotion__isnull=False).count()

# Check buyer orders
for buyer in Buyer.objects.all()[:5]:
    regular_orders = buyer.order_set.count()
    giftbox_orders = buyer.giftbox_orders.count()
    print(f"{buyer.name}: {regular_orders} regular + {giftbox_orders} gift box = {regular_orders + giftbox_orders} total")

# Check order items
from buyer.models import OrderItem
OrderItem.objects.count()

# Check addresses
Address.objects.count()
```

## Features

- **Realistic Buyer Data**: Real names, phone numbers, and addresses
- **Mixed Order Types**: Regular products, promotions, and gift boxes
- **COD Payment**: All orders use Cash on Delivery as requested
- **Promotion Integration**: Orders with promotions and proper discount calculation
- **Gift Box Integration**: Orders with gift box campaigns and additional products
- **Data Validation**: Comprehensive integrity checks
- **Error Handling**: Graceful handling of missing data
- **Progress Tracking**: Real-time progress updates
- **Summary Reports**: Complete database statistics

## Notes

- Script uses `get_or_create()` to avoid duplicates
- If buyers/orders already exist, they won't be recreated
- Script includes comprehensive error handling and validation
- All foreign key relationships are properly maintained
- Script is designed to be run multiple times safely
- All orders use COD payment method as requested
- Realistic delivery dates and order statuses

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

5. **Run product attribute script:**
   ```bash
   python populate_product_attributes.py
   ```

6. **Run buyer and order script:**
   ```bash
   python populate_buyers_and_orders.py
   ```

This will give you a fully populated MarketVibe database with:
- 9 main categories with 90 subcategories
- 270+ brands
- 20 seller accounts
- 100 products
- 10 gift box campaigns
- 35+ seller campaign participations
- 5 product promotions
- 450+ product attribute values
- 20 buyer accounts
- 60 orders (40 regular + 20 gift box)
- 120 order items
- 20 buyer addresses
- 45 buyer notifications 