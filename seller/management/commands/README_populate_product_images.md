# Populate Product Images

This script populates the MarketVibe database with product images for existing products.

## Overview

The script creates category-specific product images using the PIL (Python Imaging Library) to generate:
- **Thumbnail images** (marked as primary images)
- **Additional product images** (different angles/views)
- **Category-specific styling** with appropriate colors and icons

## Features

### Category-Specific Styling
Each product category gets its own visual style:
- **Electronics**: Blue/Green themes with tech icons (📱💻⌚📺🔊📷🎧🔋🎮🚁)
- **Automobiles**: Red/Orange themes with vehicle icons (🚗🏍️🛴🔧🛞⚡🪖🎵🚛🚙)
- **Clothing**: Various color themes with clothing icons (👕👗👖👚👶👟🧥🧦🧢👔)

### Image Generation
- Creates 3 images per product (1 thumbnail + 2 additional)
- Different sizes and angles for variety
- High-quality JPEG format (85% quality)
- Stored as binary data (BLOB) in the database

### Smart Processing
- Skips products that already have images
- Updates main product image field with thumbnail
- Provides detailed progress reporting

## Prerequisites

### Required Python Packages
```bash
pip install Pillow
```

### Database Requirements
- Products must exist in the database
- Categories and brands should be populated
- Run the following scripts first:
  1. `populate_categories.py`
  2. `populate_brands.py`
  3. `populate_sellers_and_products.py`

## Usage

### Basic Usage
```bash
python populate_product_images.py
```

### What the Script Does
1. **Checks for existing products** - Ensures products exist before processing
2. **Creates category-specific images** - Generates styled images based on product category
3. **Adds multiple images per product** - Creates thumbnail + additional images
4. **Updates product main image** - Sets the thumbnail as the main product image
5. **Provides detailed reporting** - Shows progress and statistics

### Expected Output
```
Starting to populate database with product images...
============================================================
Found 100 products to process
============================================================

Processing: Samsung Premium Smartphone (Smartphones)
    ✓ Created thumbnail image
    ✓ Created additional image 1
    ✓ Created additional image 2
    ✓ Updated main product image
    ✅ Successfully added 3 images

Processing: Apple Flagship Mobile (Smartphones)
    ✓ Created thumbnail image
    ✓ Created additional image 1
    ✓ Created additional image 2
    ✓ Updated main product image
    ✅ Successfully added 3 images

...

============================================================
✅ Successfully processed 100 products
✅ Successfully created 300 product images
📊 Average images per product: 3.0
============================================================

📈 Database Summary:
   • Total Products: 100
   • Products with Images: 100
   • Total Product Images: 300
   • Thumbnail Images: 100

🖼️ Sample Products with Images:
   • Samsung Premium Smartphone - 3 images (thumbnail: 1)
   • Apple Flagship Mobile - 3 images (thumbnail: 2)
   • Sony Gaming Laptop - 3 images (thumbnail: 3)
   • Canon DSLR Camera - 3 images (thumbnail: 4)
   • Nike Running Shoes - 3 images (thumbnail: 5)
```

## Database Impact

### Models Updated
- **Product**: Main image field updated with thumbnail
- **ProductImage**: New records created for each image

### Image Storage
- Images stored as `BinaryField` (BLOB) in database
- Base64 encoded for display in templates
- Optimized JPEG format for web display

## Customization

### Modify Image Styles
Edit the `category_styles` dictionary in the script to change:
- Background colors
- Text colors
- Category icons

### Change Image Count
Modify the `num_images` parameter in `add_images_to_product()` to create more/fewer images per product.

### Adjust Image Quality
Change the `quality` parameter in `image_to_binary()` to adjust JPEG compression.

## Troubleshooting

### Common Issues

1. **"No products found"**
   - Run `populate_sellers_and_products.py` first
   - Ensure categories and brands are populated

2. **PIL/Pillow not installed**
   ```bash
   pip install Pillow
   ```

3. **Font issues**
   - The script falls back to default fonts if Arial is not available
   - Images will still be generated with basic text rendering

4. **Memory issues with large datasets**
   - Process products in smaller batches
   - Reduce image quality or size if needed

### Verification
After running the script, verify images are working:
1. Check Django admin for product images
2. View product pages in the web interface
3. Verify base64 encoding works in templates

## File Structure
```
MarketVibe/
├── populate_product_images.py          # Main script
├── README_populate_product_images.md   # This file
└── seller/
    ├── models.py                      # Product and ProductImage models
    └── templates/
        └── seller/
            └── product_list.html       # Template showing images
```

## Related Scripts
- `populate_categories.py` - Creates product categories
- `populate_brands.py` - Creates product brands  
- `populate_sellers_and_products.py` - Creates sellers and products
- `populate_product_attributes.py` - Adds product attributes

## Notes
- Images are generated programmatically, not real product photos
- Designed for development/testing purposes
- Can be extended to use real product images from URLs or file uploads
- Follows the project's BinaryField image storage pattern 