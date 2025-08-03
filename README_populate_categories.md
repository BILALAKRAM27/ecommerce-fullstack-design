# Category and Attribute Population Scripts

This directory contains scripts to populate the MarketVibe database with categories and their attributes.

## Files

1. `populate_categories.py` - Populates Electronics, Automobiles, and Clothing categories
2. `populate_categories_part2.py` - Populates remaining categories (Home Interiors, Computer and Tech, Tools and Equipment, Sports and Outdoor, Animals and Pets, Machinery Tools)

## How to Run

### Prerequisites
- Make sure you have Django set up and the database is migrated
- Ensure you're in the Django project root directory (where `manage.py` is located)

### Running the Scripts

1. **First, run the first script:**
   ```bash
   python populate_categories.py
   ```

2. **Then run the second script:**
   ```bash
   python populate_categories_part2.py
   ```

### What the Scripts Do

These scripts will create:

#### Main Categories:
- 📦 Electronics
- 🚗 Automobiles  
- 👕 Clothes and Wear
- 🛋️ Home Interiors
- 💻 Computer and Tech
- 🧰 Tools and Equipment
- 🏀 Sports and Outdoor
- 🐾 Animals and Pets
- ⚙️ Machinery Tools

#### Each category will have multiple subcategories with specific attributes:

**Example for Smartphones (Electronics):**
- Brand (dropdown): Apple, Samsung, Xiaomi, Oppo
- RAM (dropdown): 4, 6, 8, 12 GB
- Storage (dropdown): 64, 128, 256, 512 GB
- Battery Capacity (number): mAh
- 5G Support (boolean): Yes, No

**Example for Cars (Automobiles):**
- Brand (dropdown): Toyota, Honda, Kia, Hyundai
- Fuel Type (dropdown): Petrol, Diesel, Hybrid, Electric
- Transmission (dropdown): Manual, Automatic
- Engine Capacity (number): cc

## Input Types Used

- **TEXT**: Free text input
- **NUMBER**: Numeric input with optional units (e.g., "inches", "GB", "mAh")
- **DROPDOWN**: Select from predefined options
- **BOOLEAN**: Yes/No radio buttons

## Database Models Used

- `Category`: Main and subcategories
- `CategoryAttribute`: Attributes for each category
- `AttributeOption`: Options for dropdown attributes
- `InputType`: Type of input (text, number, dropdown, boolean)

## Notes

- Scripts use `get_or_create()` to avoid duplicates
- If categories/attributes already exist, they won't be recreated
- All scripts include proper error handling and progress messages
- The scripts are designed to be run multiple times safely

## Verification

After running the scripts, you can verify the data was created by:

1. Using Django admin interface
2. Running Django shell and querying the models
3. Checking your database directly

Example Django shell commands:
```python
from seller.models import Category, CategoryAttribute

# Check main categories
Category.objects.filter(parent=None).values_list('name', flat=True)

# Check subcategories
Category.objects.filter(parent__name='Electronics').values_list('name', flat=True)

# Check attributes for a specific category
smartphones = Category.objects.get(name='Smartphones')
smartphones.attributes.all().values_list('name', 'input_type')
``` 