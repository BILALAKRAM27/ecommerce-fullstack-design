# Django Management Commands

This directory contains Django management commands for populating the database with sample data.

## Category Population Scripts

### 1. `populate_categories.py` (Main Script)
**Usage:** `python manage.py populate_categories`

This is the main comprehensive script that populates the database with all categories, subcategories, and attributes. It includes:

- **8 Main Categories**: Automobiles, Clothes and Wear, Home Interiors, Computer and Tech, Tools and Equipment, Sports and Outdoor, Animals and Pets, Machinery Tools
- **40 Subcategories**: 5 subcategories per main category
- **200 Attributes**: 5 attributes per subcategory
- **985 Attribute Options**: Various options for each attribute

**Features:**
- Uses `get_or_create()` to prevent duplicate entries
- Can be run multiple times safely
- Provides detailed output of what was created
- Includes summary statistics

### 2. `populate_categories_legacy.py` (Legacy Script)
**Usage:** `python manage.py populate_categories_legacy`

This is the original simple script that creates basic categories:
- Electronics (with Mobile Phones and Laptops subcategories)
- Clothing (with Men's and Women's Clothing subcategories)

**Features:**
- Uses `get_or_create()` for safe re-runs
- Creates basic attributes like RAM, Storage, Color, Size, etc.
- Useful for testing or minimal setups

### 3. `populate_comprehensive_categories.py` (Alternative)
**Usage:** `python manage.py populate_comprehensive_categories`

This is an alternative comprehensive script with the same functionality as the main script.

## Attribute Options Scripts

### `populate_attribute_options.py`
**Usage:** `python manage.py populate_attribute_options`

Populates additional attribute options for existing categories. Useful for extending existing data.

## Other Population Scripts

### `populate_activities_notifications.py`
**Usage:** `python manage.py populate_activities_notifications`

Creates sample activities and notifications for sellers.

### `populate_buyer_notifications.py`
**Usage:** `python manage.py populate_buyer_notifications`

Creates sample notifications for buyers.

### `populate_dashboard_data.py`
**Usage:** `python manage.py populate_dashboard_data`

Populates dashboard with sample data for testing.

### `fix_promotions.py`
**Usage:** `python manage.py fix_promotions`

Fixes promotion-related data issues.

### `populate_brands.py`
**Usage:** `python manage.py populate_brands`

Populates the database with a comprehensive list of 32 popular brands across different industries including:
- **Electronics & Tech**: Samsung, Sony, LG, Apple, Dell, HP
- **Fashion & Clothing**: Levi, Zara, Nike, Adidas, H&M, Alkaram
- **Automotive**: Toyota, Tesla, Honda, BMW, Mercedes
- **Home & Furniture**: IKEA, Ashley HomeStore, West Elm
- **Tools & Equipment**: DeWalt, Makita, Bosch
- **Sports & Outdoor**: Decathlon, Columbia, The North Face
- **Pet Supplies**: Pedigree, Whiskas, Trixie
- **Heavy Machinery**: Caterpillar (CAT), John Deere, Komatsu

**Features:**
- Uses `get_or_create()` to prevent duplicate entries
- Can be run multiple times safely
- Provides detailed output of what was created
- Includes summary statistics

### `populate_all_data.py` (Recommended)
**Usage:** `python manage.py populate_all_data`

This is the recommended script for first-time setup. It populates both categories and brands in one command:
- Runs `populate_categories` to create all categories, subcategories, and attributes
- Runs `populate_brands` to create all brands
- Provides a comprehensive summary

**Perfect for:**
- Initial database setup
- Fresh installations
- Complete data population

## Usage Guidelines

1. **First Time Setup** (Recommended): 
   - Run `python manage.py populate_all_data` to create everything at once
   
   **OR** (Individual scripts):
   - Run `python manage.py populate_categories` to create all categories
   - Run `python manage.py populate_brands` to create all brands
   
2. **Safe Re-runs**: All scripts use `get_or_create()` so they can be run multiple times
3. **Verbose Output**: Add `--verbosity=2` for detailed output
4. **Testing**: Use legacy script for minimal testing setups

## Category Structure

The comprehensive script creates the following structure:

```
Automobiles
├── Cars
├── Motorcycles
├── Car Accessories
├── Tyres & Rims
└── Auto Electronics

Clothes and Wear
├── Men's Clothing
├── Women's Clothing
├── Kids' Wear
├── Shoes
└── Accessories

Home Interiors
├── Furniture
├── Lighting
├── Wall Decor
├── Bedding
└── Kitchen Essentials

Computer and Tech
├── Laptops
├── Desktop Computers
├── Computer Accessories
├── Mobile Phones
└── Smart Devices

Tools and Equipment
├── Power Tools
├── Hand Tools
├── Garden Tools
├── Industrial Equipment
└── Measuring Tools

Sports and Outdoor
├── Sportswear
├── Fitness Equipment
├── Camping Gear
├── Bicycles
└── Balls & Rackets

Animals and Pets
├── Pet Food
├── Pet Accessories
├── Grooming Products
├── Pet Toys
└── Veterinary Supplies

Machinery Tools
├── Construction Machines
├── Agricultural Tools
├── Heavy Equipment
├── Industrial Machinery
└── Generators
```

Each subcategory has 5 relevant attributes with appropriate options. 