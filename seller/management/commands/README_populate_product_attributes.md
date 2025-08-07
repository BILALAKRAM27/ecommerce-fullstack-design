# Product Attribute Values Population Script

This script populates the MarketVibe database with product attribute values based on the categories, attributes, and products we've already created.

## File

- `populate_product_attributes.py` - Populates product attribute values

## Prerequisites

**IMPORTANT**: You must run all the previous population scripts first:

1. **Categories**: Run `populate_categories.py` and `populate_categories_part2.py`
2. **Brands**: Run `populate_brands.py`
3. **Sellers and Products**: Run `populate_sellers_and_products.py`
4. **Gift Box and Promotions**: Run `populate_giftbox_and_promotions.py`
5. **Then**: Run this product attribute script

## How to Run

### Prerequisites
- Make sure you have Django set up and the database is migrated
- Ensure you're in the Django project root directory (where `manage.py` is located)
- **Must run all previous population scripts first**

### Running the Script

```bash
python populate_product_attributes.py
```

## What the Script Does

### 🔧 **Product Attribute Value Generation**

The script generates realistic attribute values for each product based on:

- **Product Category**: Uses the category's defined attributes
- **Attribute Type**: Generates appropriate values based on input type
- **Product Name**: Uses product name to generate relevant values
- **Realistic Data**: Creates values that make sense for each attribute

### 📊 **Attribute Types Handled**

#### **NUMBER Attributes**
- **RAM**: 4, 6, 8, 12, 16 GB
- **Storage/Capacity**: 64, 128, 256, 512, 1024 GB
- **Battery**: 3000, 4000, 5000, 6000, 7000 mAh
- **Screen Size**: 5, 6, 7, 8, 10, 13, 15, 17 inches
- **Weight**: 100, 150, 200, 250, 300, 500 grams
- **Dimensions**: Length, Width, Height, Thickness
- **Technical Specs**: Voltage, Power, Speed, Pressure, Temperature
- **Performance**: Current, Flow, Capacity, Frequency

#### **BOOLEAN Attributes**
- **Features**: Waterproof, Wireless, Bluetooth, WiFi, Smart, Touch
- **Functionality**: Backlit, Adjustable, Foldable, Recliner, Storage
- **Quality**: Lockable, Framed, Retractable, Washable, Certified
- **Technology**: GPS, Fast Charging, Solar, Reversible, Universal
- **Design**: Hooded, Non-slip, Scented, Magnetic, Auto

#### **TEXT Attributes**
- **Brand**: Extracted from product name
- **Color**: Black, White, Blue, Red, Green, Silver, Gold, Gray, Brown, Pink
- **Material**: Plastic, Metal, Wood, Glass, Fabric, Leather, Rubber, Aluminum, Steel, Carbon Fiber
- **Type**: Standard, Premium, Professional, Basic, Advanced, Compact, Portable, Fixed
- **Style**: Modern, Classic, Vintage, Contemporary, Traditional, Minimalist, Luxury
- **Pattern**: Solid, Striped, Floral, Geometric, Abstract, Plain, Printed
- **Connection**: Wired, Wireless, Bluetooth, USB, HDMI, WiFi
- **Light Source**: LED, LCD, OLED, CFL, Halogen, Incandescent
- **Fuel Type**: Petrol, Diesel, Electric, Hybrid, Gas, Battery
- **Transmission**: Manual, Automatic, CVT, Semi-Auto
- **Fit**: Slim, Regular, Loose, Skinny, Relaxed, Standard
- **Wash**: Light, Medium, Dark, Stone, Acid, Regular
- **Neck Type**: Round, V-neck, Collar, Boat, Crew, Scoop
- **Sleeve Type**: Full, Half, 3/4th, Sleeveless, Short, Long
- **Sole Material**: Rubber, EVA, PU, Leather, Synthetic
- **Strap Type**: Velcro, Lace-up, Elastic, Buckle, Hook
- **Buckle Type**: Pin, Automatic, Reversible, Standard, Quick-release
- **Stud Type**: Firm Ground, Soft Ground, Turf, Indoor, Artificial
- **Willow Type**: English, Kashmir, Premium, Standard
- **Panel Type**: IPS, TN, VA, OLED, QLED
- **Resolution**: HD, Full HD, 2K, 4K, 8K, 720p, 1080p
- **DPI Range**: 800-1600, 1600-3200, 3200-6400, 1000-2000
- **Function**: Print, Print + Scan, All-in-One, Copy, Fax
- **WiFi Band**: Single, Dual, Tri-band, 2.4GHz, 5GHz
- **Connection Type**: USB 2.0, 3.0, Type-C, Thunderbolt, FireWire
- **Mount Type**: Clip-on, Tripod, Wall, Ceiling, Table
- **Channel Configuration**: 2.0, 2.1, 5.1, 7.1, Stereo, Mono
- **License Duration**: 1 Year, 3 Years, Lifetime, Perpetual, Subscription
- **Platform**: Windows, Mac, Linux, Cross-platform, Mobile
- **Power Type**: Corded, Cordless, Battery, Electric, Manual
- **Phase**: Single, Three, Dual, Multi
- **Control Type**: Manual, Automatic, Digital, Analog, Remote
- **Engine Type**: Petrol, Diesel, Electric, Hybrid, Gas
- **Duty Cycle**: Continuous, Intermittent, Heavy, Light, Standard
- **Crane Type**: Gantry, Overhead, Jib, Mobile, Tower
- **Glass Type**: Acrylic, Glass, Tempered, Laminated, Float
- **Filter Type**: Mechanical, Biological, Chemical, UV, Carbon
- **Pump Type**: Electric, Diesel, Solar, Manual, Submersible
- **Vacuum Type**: Wet & Dry, Dry Only, HEPA, Bagless, Cordless
- **Generator Type**: Petrol, Diesel, Gas, Solar, Wind
- **Handling Type**: Gantry, Overhead, Jib, Mobile, Tower

#### **DROPDOWN Attributes**
- Uses existing attribute options from the database
- Falls back to "Default" if no options are available

## Database Models Used

- `Product`: Existing products
- `CategoryAttribute`: Category attributes (from previous scripts)
- `ProductAttributeValue`: Links products to attribute values
- `AttributeOption`: Dropdown options (from previous scripts)
- `InputType`: Attribute input types

## Expected Output

```
Starting to populate Product Attribute Values...
============================================================
📦 Found 100 products to populate with attributes

Processing product 1/100: Samsung Premium Smartphone
  ✓ Brand: Samsung
  ✓ RAM: 8
  ✓ Storage: 256
  ✓ Battery Capacity: 4500
  ✓ 5G Support: Yes
  📊 Created 5 attributes for this product

Processing product 2/100: Apple Gaming Laptop
  ✓ Brand: Apple
  ✓ Processor: Intel i7
  ✓ RAM: 16
  ✓ Storage Type: SSD
  ✓ Graphics Card: NVIDIA RTX 3060
  ✓ Screen Size: 15
  📊 Created 6 attributes for this product

...

============================================================
✅ Product Attribute Values populated successfully!
============================================================

📈 Summary:
   • Total Products Processed: 100
   • Products with Attributes: 100
   • Total Attribute Values Created: 450
   • Average Attributes per Product: 4.5

🔍 Sample Attribute Values:
   • Samsung Premium Smartphone:
     - Brand: Samsung
     - RAM: 8
     - Storage: 256
   • Apple Gaming Laptop:
     - Brand: Apple
     - Processor: Intel i7
     - RAM: 16
   • Nike Cotton T-Shirt:
     - Brand: Nike
     - Size: M
     - Material: Cotton
     - Sleeve Type: Half
     - Fit: Regular

🔍 Validating Attribute Data...
✓ Total Attribute Values: 450
✓ Products with Attributes: 100/100

📊 Attribute Distribution by Category:
   • Smartphones: 50 values for 10 products
   • Laptops: 60 values for 10 products
   • Men's T-Shirts: 40 values for 8 products
   • Women's Dresses: 35 values for 7 products
   • Cars: 30 values for 6 products
   • Bikes: 25 values for 5 products
   ...

📋 Attribute Types Distribution:
   • text: 180 values
   • number: 150 values
   • dropdown: 80 values
   • boolean: 40 values
```

## Data Integrity Validation

The script includes comprehensive validation to ensure:

### ✅ **Product-Category Matching**
- Each product gets attributes from its assigned category
- No orphaned attribute values
- All products have appropriate attributes

### ✅ **Attribute Type Compliance**
- NUMBER attributes get realistic numeric values
- BOOLEAN attributes get Yes/No values
- TEXT attributes get relevant text values
- DROPDOWN attributes use existing options

### ✅ **Realistic Data Generation**
- Values are appropriate for the attribute name
- Numbers are within realistic ranges
- Text values are relevant to the product type
- Boolean values make sense for the feature

### ✅ **Foreign Key Relationships**
- All product-attribute relationships are valid
- All attribute-category relationships are maintained
- No orphaned records

## Verification

After running the script, you can verify the data was created by:

1. **Django Admin Interface**: Check ProductAttributeValue model
2. **Django Shell**: Query the models directly
3. **Database**: Check the database tables

Example Django shell commands:
```python
from seller.models import Product, ProductAttributeValue, CategoryAttribute

# Check total attribute values
ProductAttributeValue.objects.count()

# Check products with attributes
products_with_attrs = Product.objects.filter(attribute_values__isnull=False).distinct()
print(f"Products with attributes: {products_with_attrs.count()}")

# Check attribute distribution by category
for product in Product.objects.all()[:5]:
    attrs = product.attribute_values.all()
    print(f"{product.name} ({product.category.name}): {attrs.count()} attributes")
    for attr in attrs[:3]:
        print(f"  - {attr.attribute.name}: {attr.value}")

# Check attribute types
attr_types = ProductAttributeValue.objects.values_list('attribute__input_type', flat=True).distinct()
for attr_type in attr_types:
    count = ProductAttributeValue.objects.filter(attribute__input_type=attr_type).count()
    print(f"{attr_type}: {count} values")
```

## Features

- **Smart Value Generation**: Creates realistic values based on attribute names
- **Category-Aware**: Uses category-specific attributes for each product
- **Type Compliance**: Generates appropriate values for each input type
- **Realistic Data**: Values that make sense for the product type
- **Data Validation**: Comprehensive integrity checks
- **Error Handling**: Graceful handling of missing data
- **Progress Tracking**: Real-time progress updates
- **Summary Reports**: Complete database statistics

## Notes

- Script uses `get_or_create()` to avoid duplicates
- If attribute values already exist, they will be updated
- Script includes comprehensive error handling and validation
- All foreign key relationships are properly maintained
- Script is designed to be run multiple times safely
- Values are generated based on attribute names and types
- Realistic ranges are used for numeric values

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

This will give you a fully populated MarketVibe database with:
- 9 main categories with 90 subcategories
- 270+ brands
- 20 seller accounts
- 100 products
- 10 gift box campaigns
- 35+ seller campaign participations
- 5 product promotions
- 450+ product attribute values 