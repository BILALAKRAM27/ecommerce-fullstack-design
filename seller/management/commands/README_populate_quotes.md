# Quote Population Script

This script populates the MarketVibe database with realistic quote requests from buyers and quote responses from sellers.

## 📋 What This Script Does

### Quote Requests (30 requests)
- Creates realistic quote requests from existing buyers
- Covers various product categories and industries
- Includes different urgency levels and budget ranges
- Sets appropriate delivery deadlines and expiration dates

### Quote Responses (Multiple per request)
- Generates responses from 1-3 sellers per quote request
- Calculates realistic pricing based on urgency and quantity
- Provides delivery estimates and seller notes
- Sets acceptance/rejection status for responses

## 🚀 Prerequisites

Before running this script, ensure you have:

1. **Buyers**: Run `populate_buyers_and_orders.py` first
2. **Sellers**: Run `populate_sellers_and_products.py` first  
3. **Categories**: Run `populate_categories.py` and `populate_categories_part2.py` first

## 📝 Usage

```bash
python populate_quotes.py
```

## 🎯 Features

### Quote Request Features
- **Realistic Product Names**: Custom electronics, bulk clothing, industrial machinery, etc.
- **Category Matching**: Automatically matches requests to appropriate categories
- **Varied Quantities**: Ranges from 1 to 500 units depending on product type
- **Budget Ranges**: Realistic budget expectations ($300-$15,000)
- **Urgency Levels**: Low, Medium, High, Urgent
- **Delivery Deadlines**: 1-60 days from creation
- **Expiration Dates**: 7-30 days from creation

### Quote Response Features
- **Smart Pricing**: Adjusts based on urgency and quantity
- **Quantity Discounts**: 10-20% discount for bulk orders
- **Urgency Premiums**: 15-30% premium for urgent orders
- **Delivery Estimates**: Realistic delivery times based on urgency
- **Seller Notes**: Professional responses with relevant information
- **Status Management**: Automatic acceptance/rejection logic

### Data Integrity Features
- **Prerequisite Validation**: Checks for required data before running
- **Realistic Relationships**: Links to existing buyers, sellers, and categories
- **Status Consistency**: Updates quote request statuses based on responses
- **Comprehensive Validation**: Detailed reporting of created data

## 📊 Expected Output

### Quote Requests Created
- **30 Quote Requests** across various categories
- **Realistic product descriptions** and requirements
- **Varied urgency levels** and budget ranges
- **Proper category assignments** based on product type

### Quote Responses Created
- **60-90 Quote Responses** (2-3 per request)
- **Realistic pricing** with quantity and urgency adjustments
- **Professional seller notes** and delivery estimates
- **Status distribution**: ~33% accepted, ~33% rejected, ~33% pending

### Validation Report
- Quote request and response counts
- Status distribution analysis
- Category distribution summary
- Average responses per request
- Sample data preview

## 🔍 Verification

After running the script, you can verify the data:

### Check Quote Requests
```python
from seller.models import QuoteRequest
QuoteRequest.objects.count()  # Should be 30
```

### Check Quote Responses  
```python
from seller.models import QuoteResponse
QuoteResponse.objects.count()  # Should be 60-90
```

### Check Status Distribution
```python
QuoteRequest.objects.filter(status='accepted').count()
QuoteRequest.objects.filter(status='responded').count()
QuoteRequest.objects.filter(status='rejected').count()
```

### Check Response Distribution
```python
QuoteResponse.objects.filter(is_accepted=True).count()
QuoteResponse.objects.filter(is_rejected=True).count()
QuoteResponse.objects.filter(is_accepted=False, is_rejected=False).count()
```

## 📈 Sample Data Created

### Quote Request Examples
- **Custom Electronics Assembly**: 10-100 units, $500-$2000 budget
- **Bulk Clothing Order**: 50-500 units, $1000-$5000 budget  
- **Industrial Machinery Parts**: 5-25 units, $2000-$10000 budget
- **Home Interior Furniture**: 1-10 units, $500-$3000 budget
- **Sports Equipment Bulk Order**: 20-100 units, $800-$4000 budget

### Quote Response Examples
- **Pricing**: $10-$500 per unit with quantity discounts
- **Delivery**: 1-30 days based on urgency
- **Notes**: Professional responses with quality guarantees
- **Status**: Mix of accepted, rejected, and pending responses

## 🛠️ Technical Details

### Models Used
- `QuoteRequest`: Buyer quote requests with product details
- `QuoteResponse`: Seller responses with pricing and delivery info
- `Buyer`: Links to existing buyer accounts
- `Seller`: Links to existing seller accounts  
- `Category`: Links to appropriate product categories

### Key Features
- **Realistic Pricing Logic**: Base price adjusted by urgency and quantity
- **Smart Category Matching**: Uses keywords to find appropriate categories
- **Status Management**: Automatically updates request statuses based on responses
- **Data Validation**: Comprehensive checks and reporting

## ✅ Success Indicators

The script runs successfully when you see:
- ✅ All prerequisite checks pass
- ✅ Quote requests created with realistic data
- ✅ Quote responses generated with proper pricing
- ✅ Status updates completed
- ✅ Validation report shows expected counts
- ✅ Final summary displays sample data

## 🔧 Troubleshooting

### Common Issues
1. **"No buyers found"**: Run buyer population script first
2. **"No sellers found"**: Run seller population script first  
3. **"No categories found"**: Run category population scripts first
4. **Import errors**: Ensure Django environment is properly set up

### Data Verification
- Check that quote requests link to existing buyers and categories
- Verify that quote responses link to existing sellers
- Confirm that pricing and delivery estimates are realistic
- Ensure status updates are working correctly

## 📚 Related Scripts

This script is part of the complete MarketVibe database population suite:

1. `populate_categories.py` - Product categories and attributes
2. `populate_categories_part2.py` - Additional categories
3. `populate_brands.py` - Product brands
4. `populate_sellers_and_products.py` - Seller accounts and products
5. `populate_giftbox_and_promotions.py` - Gift box campaigns and promotions
6. `populate_product_attributes.py` - Product attribute values
7. `populate_buyers_and_orders.py` - Buyer accounts and orders
8. **`populate_quotes.py`** - Quote requests and responses (this script)

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

# 7. Quotes (this script)
python populate_quotes.py
```

This will create a fully populated MarketVibe database with realistic test data for all major features! 