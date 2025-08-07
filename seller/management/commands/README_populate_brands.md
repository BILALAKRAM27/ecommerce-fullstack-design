# Brand Population Script

This script populates the MarketVibe database with brands for all categories and subcategories.

## File

- `populate_brands.py` - Populates brands for all categories

## How to Run

### Prerequisites
- Make sure you have Django set up and the database is migrated
- Ensure you're in the Django project root directory (where `manage.py` is located)
- **Important**: Run the category population scripts first before running this brand script

### Running the Script

```bash
python populate_brands.py
```

### What the Script Does

This script will create brands for all categories and subcategories:

#### 📦 Electronics
- **Smartphones**: Samsung, Apple, Xiaomi
- **Laptops**: HP, Dell, Lenovo
- **Smart Watches**: Apple, Fitbit, Samsung
- **LED TVs**: Sony, LG, TCL
- **Bluetooth Speakers**: JBL, Bose, Anker
- **Cameras**: Canon, Nikon, Sony
- **Headphones**: Sony, JBL, Beats
- **Power Banks**: Anker, Xiaomi, Realme
- **Gaming Consoles**: Sony, Microsoft, Nintendo
- **Drones**: DJI, Autel, Parrot

#### 🚗 Automobiles
- **Cars**: Toyota, Honda, Kia
- **Bikes**: Yamaha, Suzuki, Honda
- **Electric Scooters**: Segway, Xiaomi, Hero Electric
- **Car Accessories**: Autofy, Michelin, GoMechanic
- **Tyres**: Michelin, Bridgestone, Dunlop
- **Car Batteries**: Exide, Amaron, Bosch
- **Motorbike Helmets**: Studds, Vega, Steelbird
- **Car Audio Systems**: Sony, Pioneer, Blaupunkt
- **Truck Parts**: Bosch, Denso, Hino
- **SUV Accessories**: Rhino, Thule, Autoform

#### 👕 Clothes and Wear
- **Men's T-Shirts**: Nike, Adidas, Puma
- **Women's Dresses**: Zara, H&M, Forever 21
- **Men's Jeans**: Levi's, Wrangler, Lee
- **Women's Tops**: Only, Mango, H&M
- **Children's Clothing**: Mothercare, Carter's, Babyshop
- **Footwear**: Bata, Adidas, Skechers
- **Winter Jackets**: Columbia, North Face, Zara
- **Socks**: Nike, Puma, Hanes
- **Caps and Hats**: New Era, Nike, Adidas
- **Belts**: Allen Solly, Levi's, Hidesign

#### 🛋️ Home Interiors
- **Sofas**: IKEA, Urban Ladder, Home Centre
- **Beds**: Pepperfry, Wakefit, Durian
- **Curtains**: Spaces, Story@Home, Raymond
- **Wall Clocks**: Ajanta, Casio, Seiko
- **Ceiling Lights**: Philips, Wipro, Havells
- **Dining Tables**: Nilkamal, Urban Ladder, IKEA
- **Rugs**: Safavieh, IKEA, Saral Home
- **Storage Cabinets**: Godrej, Nilkamal, HomeTown
- **Wall Art**: DecorsMania, Wallmantra, PosterGully
- **Lamps**: Philips, Syska, IKEA

#### 💻 Computer and Tech
- **Desktops**: HP, Lenovo, Dell
- **Monitors**: LG, Dell, Samsung
- **Keyboards**: Logitech, Redragon, HP
- **Mice**: Logitech, Razer, HP
- **Printers**: Canon, HP, Epson
- **Routers**: TP-Link, Netgear, D-Link
- **External Hard Drives**: Seagate, WD, Toshiba
- **Webcams**: Logitech, HP, Ausdom
- **Computer Speakers**: Creative, JBL, Zebronics
- **Software Packages**: Kaspersky, Microsoft, Norton

#### 🧰 Tools and Equipment
- **Power Drills**: Bosch, Black+Decker, Dewalt
- **Welding Machines**: Rilon, ESAB, Panasonic
- **Screwdriver Sets**: Stanley, Bosch, Taparia
- **Measuring Tapes**: Freemans, Stanley, Bosch
- **Air Compressors**: Elgi, Ingersoll Rand, Tiger
- **Multimeters**: Meco, Fluke, HTC
- **Ladders**: Bathla, Gorilla, Werner
- **Angle Grinders**: Makita, Bosch, Dewalt
- **Tool Kits**: Taparia, Stanley, Black+Decker
- **Chainsaws**: Stihl, Husqvarna, Makita

#### 🏀 Sports and Outdoor
- **Treadmills**: PowerMax, Durafit, Cockatoo
- **Dumbbell Sets**: Kobo, Aurion, AmazonBasics
- **Football Shoes**: Nike, Adidas, Puma
- **Bicycles**: Hero, Firefox, Trek
- **Cricket Bats**: SS, SG, Kookaburra
- **Camping Tents**: Quechua, Coleman, Wildcraft
- **Yoga Mats**: AmazonBasics, Boldfit, Adidas
- **Skates**: Nivia, Cosco, Rollerblade
- **Badminton Rackets**: Yonex, Li-Ning, Carlton
- **Boxing Gloves**: Everlast, USI, Adidas

#### 🐾 Animals and Pets
- **Dog Food**: Pedigree, Drools, Royal Canin
- **Cat Litter**: Kit Cat, Ever Clean, Me-O
- **Bird Cages**: Savic, Prevue, Yaheetech
- **Fish Tanks**: Boyu, Sobo, Marina
- **Pet Toys**: KONG, BarkBox, Trixie
- **Leashes**: PetSafe, Trixie, Fida
- **Dog Beds**: FurHaven, MidWest, AmazonBasics
- **Aquarium Accessories**: SunSun, Boyu, Aquael
- **Pet Grooming Kits**: Wahl, Petology, Andis
- **Pet Carriers**: Petmate, AmazonBasics, Ferplast

#### ⚙️ Machinery Tools
- **Industrial Generators**: Kirloskar, Cummins, Honda
- **CNC Machines**: Haas, Siemens, Mazak
- **Hydraulic Presses**: Enerpac, Dake, Baileigh
- **Lathe Machines**: HMT, ACE, Bhavya
- **Forklifts**: Toyota, CAT, Godrej
- **Air Handling Units**: Voltas, Carrier, Blue Star
- **Water Pumps**: Crompton, Kirloskar, Havells
- **Industrial Vacuum Cleaners**: Karcher, IPC, Nilfisk
- **Welding Generators**: Koike, Honda, Lincoln
- **Material Handling Cranes**: Demag, Konecranes, ElectroMech

## Database Model Used

- `Brand`: Contains brand information
  - `name` (CharField): Brand name
  - `logo_url` (URLField, optional): Brand logo URL

## Features

- **Safe Execution**: Uses `get_or_create()` to avoid duplicates
- **Error Handling**: Gracefully handles missing categories
- **Progress Tracking**: Shows progress for each category
- **Summary Report**: Displays total brands created
- **Category Validation**: Checks if categories exist before adding brands

## Notes

- Script uses `get_or_create()` to avoid duplicates
- If brands already exist, they won't be recreated
- Script includes proper error handling and progress messages
- The script is designed to be run multiple times safely
- **Must run category population scripts first** before running this brand script

## Verification

After running the script, you can verify the data was created by:

1. Using Django admin interface
2. Running Django shell and querying the models
3. Checking your database directly

Example Django shell commands:
```python
from seller.models import Brand, Category

# Check total brands
Brand.objects.count()

# Check brands for a specific category
smartphones = Category.objects.get(name='Smartphones')
print(f"Brands for Smartphones: {[b.name for b in Brand.objects.all()]}")

# Check all brands
Brand.objects.all().values_list('name', flat=True)
```

## Expected Output

```
Starting to populate brands for all categories...
==================================================
Populating Electronics brands...
✓ Added 3 brands for Smartphones
✓ Added 3 brands for Laptops
✓ Added 3 brands for Smart Watches
...

Populating Automobiles brands...
✓ Added 3 brands for Cars
✓ Added 3 brands for Bikes
...

==================================================
✅ Brand population completed successfully!
📊 Total brands in database: 270
==================================================
``` 