#!/usr/bin/env python
"""
Script to populate brands for all categories in MarketVibe
Run this script from the Django project root directory
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Category, Brand

def create_brand(name, logo_url=None):
    """Create a brand if it doesn't exist"""
    brand, created = Brand.objects.get_or_create(
        name=name,
        defaults={'logo_url': logo_url}
    )
    return brand

def get_category_by_name(name, parent_name=None):
    """Get a category by name, optionally filtering by parent"""
    if parent_name:
        parent = Category.objects.get(name=parent_name)
        return Category.objects.get(name=name, parent=parent)
    else:
        return Category.objects.get(name=name)

def populate_electronics_brands():
    """Populate brands for Electronics category and subcategories"""
    print("Populating Electronics brands...")
    
    # Smartphones
    try:
        smartphones = get_category_by_name("Smartphones", "Electronics")
        brands = ["Samsung", "Apple", "Xiaomi"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Smartphones")
    except Category.DoesNotExist:
        print("⚠️ Smartphones category not found")
    
    # Laptops
    try:
        laptops = get_category_by_name("Laptops", "Electronics")
        brands = ["HP", "Dell", "Lenovo"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Laptops")
    except Category.DoesNotExist:
        print("⚠️ Laptops category not found")
    
    # Smart Watches
    try:
        smartwatches = get_category_by_name("Smart Watches", "Electronics")
        brands = ["Apple", "Fitbit", "Samsung"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Smart Watches")
    except Category.DoesNotExist:
        print("⚠️ Smart Watches category not found")
    
    # LED TVs
    try:
        led_tvs = get_category_by_name("LED TVs", "Electronics")
        brands = ["Sony", "LG", "TCL"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for LED TVs")
    except Category.DoesNotExist:
        print("⚠️ LED TVs category not found")
    
    # Bluetooth Speakers
    try:
        bluetooth_speakers = get_category_by_name("Bluetooth Speakers", "Electronics")
        brands = ["JBL", "Bose", "Anker"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Bluetooth Speakers")
    except Category.DoesNotExist:
        print("⚠️ Bluetooth Speakers category not found")
    
    # Cameras
    try:
        cameras = get_category_by_name("Cameras", "Electronics")
        brands = ["Canon", "Nikon", "Sony"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Cameras")
    except Category.DoesNotExist:
        print("⚠️ Cameras category not found")
    
    # Headphones
    try:
        headphones = get_category_by_name("Headphones", "Electronics")
        brands = ["Sony", "JBL", "Beats"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Headphones")
    except Category.DoesNotExist:
        print("⚠️ Headphones category not found")
    
    # Power Banks
    try:
        power_banks = get_category_by_name("Power Banks", "Electronics")
        brands = ["Anker", "Xiaomi", "Realme"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Power Banks")
    except Category.DoesNotExist:
        print("⚠️ Power Banks category not found")
    
    # Gaming Consoles
    try:
        gaming_consoles = get_category_by_name("Gaming Consoles", "Electronics")
        brands = ["Sony", "Microsoft", "Nintendo"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Gaming Consoles")
    except Category.DoesNotExist:
        print("⚠️ Gaming Consoles category not found")
    
    # Drones
    try:
        drones = get_category_by_name("Drones", "Electronics")
        brands = ["DJI", "Autel", "Parrot"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Drones")
    except Category.DoesNotExist:
        print("⚠️ Drones category not found")

def populate_automobiles_brands():
    """Populate brands for Automobiles category and subcategories"""
    print("Populating Automobiles brands...")
    
    # Cars
    try:
        cars = get_category_by_name("Cars", "Automobiles")
        brands = ["Toyota", "Honda", "Kia"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Cars")
    except Category.DoesNotExist:
        print("⚠️ Cars category not found")
    
    # Bikes
    try:
        bikes = get_category_by_name("Bikes", "Automobiles")
        brands = ["Yamaha", "Suzuki", "Honda"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Bikes")
    except Category.DoesNotExist:
        print("⚠️ Bikes category not found")
    
    # Electric Scooters
    try:
        e_scooters = get_category_by_name("Electric Scooters", "Automobiles")
        brands = ["Segway", "Xiaomi", "Hero Electric"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Electric Scooters")
    except Category.DoesNotExist:
        print("⚠️ Electric Scooters category not found")
    
    # Car Accessories
    try:
        car_accessories = get_category_by_name("Car Accessories", "Automobiles")
        brands = ["Autofy", "Michelin", "GoMechanic"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Car Accessories")
    except Category.DoesNotExist:
        print("⚠️ Car Accessories category not found")
    
    # Tyres
    try:
        tyres = get_category_by_name("Tyres", "Automobiles")
        brands = ["Michelin", "Bridgestone", "Dunlop"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Tyres")
    except Category.DoesNotExist:
        print("⚠️ Tyres category not found")
    
    # Car Batteries
    try:
        car_batteries = get_category_by_name("Car Batteries", "Automobiles")
        brands = ["Exide", "Amaron", "Bosch"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Car Batteries")
    except Category.DoesNotExist:
        print("⚠️ Car Batteries category not found")
    
    # Motorbike Helmets
    try:
        helmets = get_category_by_name("Motorbike Helmets", "Automobiles")
        brands = ["Studds", "Vega", "Steelbird"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Motorbike Helmets")
    except Category.DoesNotExist:
        print("⚠️ Motorbike Helmets category not found")
    
    # Car Audio Systems
    try:
        car_audio = get_category_by_name("Car Audio Systems", "Automobiles")
        brands = ["Sony", "Pioneer", "Blaupunkt"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Car Audio Systems")
    except Category.DoesNotExist:
        print("⚠️ Car Audio Systems category not found")
    
    # Truck Parts
    try:
        truck_parts = get_category_by_name("Truck Parts", "Automobiles")
        brands = ["Bosch", "Denso", "Hino"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Truck Parts")
    except Category.DoesNotExist:
        print("⚠️ Truck Parts category not found")
    
    # SUV Accessories
    try:
        suv_accessories = get_category_by_name("SUV Accessories", "Automobiles")
        brands = ["Rhino", "Thule", "Autoform"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for SUV Accessories")
    except Category.DoesNotExist:
        print("⚠️ SUV Accessories category not found")

def populate_clothing_brands():
    """Populate brands for Clothes and Wear category and subcategories"""
    print("Populating Clothing brands...")
    
    # Men's T-Shirts
    try:
        mens_tshirts = get_category_by_name("Men's T-Shirts", "Clothes and Wear")
        brands = ["Nike", "Adidas", "Puma"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Men's T-Shirts")
    except Category.DoesNotExist:
        print("⚠️ Men's T-Shirts category not found")
    
    # Women's Dresses
    try:
        womens_dresses = get_category_by_name("Women's Dresses", "Clothes and Wear")
        brands = ["Zara", "H&M", "Forever 21"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Women's Dresses")
    except Category.DoesNotExist:
        print("⚠️ Women's Dresses category not found")
    
    # Men's Jeans
    try:
        mens_jeans = get_category_by_name("Men's Jeans", "Clothes and Wear")
        brands = ["Levi's", "Wrangler", "Lee"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Men's Jeans")
    except Category.DoesNotExist:
        print("⚠️ Men's Jeans category not found")
    
    # Women's Tops
    try:
        womens_tops = get_category_by_name("Women's Tops", "Clothes and Wear")
        brands = ["Only", "Mango", "H&M"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Women's Tops")
    except Category.DoesNotExist:
        print("⚠️ Women's Tops category not found")
    
    # Children's Clothing
    try:
        children_clothing = get_category_by_name("Children's Clothing", "Clothes and Wear")
        brands = ["Mothercare", "Carter's", "Babyshop"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Children's Clothing")
    except Category.DoesNotExist:
        print("⚠️ Children's Clothing category not found")
    
    # Footwear
    try:
        footwear = get_category_by_name("Footwear", "Clothes and Wear")
        brands = ["Bata", "Adidas", "Skechers"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Footwear")
    except Category.DoesNotExist:
        print("⚠️ Footwear category not found")
    
    # Winter Jackets
    try:
        winter_jackets = get_category_by_name("Winter Jackets", "Clothes and Wear")
        brands = ["Columbia", "North Face", "Zara"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Winter Jackets")
    except Category.DoesNotExist:
        print("⚠️ Winter Jackets category not found")
    
    # Socks
    try:
        socks = get_category_by_name("Socks", "Clothes and Wear")
        brands = ["Nike", "Puma", "Hanes"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Socks")
    except Category.DoesNotExist:
        print("⚠️ Socks category not found")
    
    # Caps and Hats
    try:
        caps_hats = get_category_by_name("Caps and Hats", "Clothes and Wear")
        brands = ["New Era", "Nike", "Adidas"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Caps and Hats")
    except Category.DoesNotExist:
        print("⚠️ Caps and Hats category not found")
    
    # Belts
    try:
        belts = get_category_by_name("Belts", "Clothes and Wear")
        brands = ["Allen Solly", "Levi's", "Hidesign"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Belts")
    except Category.DoesNotExist:
        print("⚠️ Belts category not found")

def populate_home_interiors_brands():
    """Populate brands for Home Interiors category and subcategories"""
    print("Populating Home Interiors brands...")
    
    # Sofas
    try:
        sofas = get_category_by_name("Sofas", "Home Interiors")
        brands = ["IKEA", "Urban Ladder", "Home Centre"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Sofas")
    except Category.DoesNotExist:
        print("⚠️ Sofas category not found")
    
    # Beds
    try:
        beds = get_category_by_name("Beds", "Home Interiors")
        brands = ["Pepperfry", "Wakefit", "Durian"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Beds")
    except Category.DoesNotExist:
        print("⚠️ Beds category not found")
    
    # Curtains
    try:
        curtains = get_category_by_name("Curtains", "Home Interiors")
        brands = ["Spaces", "Story@Home", "Raymond"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Curtains")
    except Category.DoesNotExist:
        print("⚠️ Curtains category not found")
    
    # Wall Clocks
    try:
        wall_clocks = get_category_by_name("Wall Clocks", "Home Interiors")
        brands = ["Ajanta", "Casio", "Seiko"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Wall Clocks")
    except Category.DoesNotExist:
        print("⚠️ Wall Clocks category not found")
    
    # Ceiling Lights
    try:
        ceiling_lights = get_category_by_name("Ceiling Lights", "Home Interiors")
        brands = ["Philips", "Wipro", "Havells"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Ceiling Lights")
    except Category.DoesNotExist:
        print("⚠️ Ceiling Lights category not found")
    
    # Dining Tables
    try:
        dining_tables = get_category_by_name("Dining Tables", "Home Interiors")
        brands = ["Nilkamal", "Urban Ladder", "IKEA"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Dining Tables")
    except Category.DoesNotExist:
        print("⚠️ Dining Tables category not found")
    
    # Rugs
    try:
        rugs = get_category_by_name("Rugs", "Home Interiors")
        brands = ["Safavieh", "IKEA", "Saral Home"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Rugs")
    except Category.DoesNotExist:
        print("⚠️ Rugs category not found")
    
    # Storage Cabinets
    try:
        storage_cabinets = get_category_by_name("Storage Cabinets", "Home Interiors")
        brands = ["Godrej", "Nilkamal", "HomeTown"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Storage Cabinets")
    except Category.DoesNotExist:
        print("⚠️ Storage Cabinets category not found")
    
    # Wall Art
    try:
        wall_art = get_category_by_name("Wall Art", "Home Interiors")
        brands = ["DecorsMania", "Wallmantra", "PosterGully"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Wall Art")
    except Category.DoesNotExist:
        print("⚠️ Wall Art category not found")
    
    # Lamps
    try:
        lamps = get_category_by_name("Lamps", "Home Interiors")
        brands = ["Philips", "Syska", "IKEA"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Lamps")
    except Category.DoesNotExist:
        print("⚠️ Lamps category not found")

def populate_computer_tech_brands():
    """Populate brands for Computer and Tech category and subcategories"""
    print("Populating Computer and Tech brands...")
    
    # Desktops
    try:
        desktops = get_category_by_name("Desktops", "Computer and Tech")
        brands = ["HP", "Lenovo", "Dell"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Desktops")
    except Category.DoesNotExist:
        print("⚠️ Desktops category not found")
    
    # Monitors
    try:
        monitors = get_category_by_name("Monitors", "Computer and Tech")
        brands = ["LG", "Dell", "Samsung"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Monitors")
    except Category.DoesNotExist:
        print("⚠️ Monitors category not found")
    
    # Keyboards
    try:
        keyboards = get_category_by_name("Keyboards", "Computer and Tech")
        brands = ["Logitech", "Redragon", "HP"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Keyboards")
    except Category.DoesNotExist:
        print("⚠️ Keyboards category not found")
    
    # Mice
    try:
        mice = get_category_by_name("Mice", "Computer and Tech")
        brands = ["Logitech", "Razer", "HP"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Mice")
    except Category.DoesNotExist:
        print("⚠️ Mice category not found")
    
    # Printers
    try:
        printers = get_category_by_name("Printers", "Computer and Tech")
        brands = ["Canon", "HP", "Epson"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Printers")
    except Category.DoesNotExist:
        print("⚠️ Printers category not found")
    
    # Routers
    try:
        routers = get_category_by_name("Routers", "Computer and Tech")
        brands = ["TP-Link", "Netgear", "D-Link"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Routers")
    except Category.DoesNotExist:
        print("⚠️ Routers category not found")
    
    # External Hard Drives
    try:
        external_hdds = get_category_by_name("External Hard Drives", "Computer and Tech")
        brands = ["Seagate", "WD", "Toshiba"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for External Hard Drives")
    except Category.DoesNotExist:
        print("⚠️ External Hard Drives category not found")
    
    # Webcams
    try:
        webcams = get_category_by_name("Webcams", "Computer and Tech")
        brands = ["Logitech", "HP", "Ausdom"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Webcams")
    except Category.DoesNotExist:
        print("⚠️ Webcams category not found")
    
    # Computer Speakers
    try:
        computer_speakers = get_category_by_name("Computer Speakers", "Computer and Tech")
        brands = ["Creative", "JBL", "Zebronics"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Computer Speakers")
    except Category.DoesNotExist:
        print("⚠️ Computer Speakers category not found")
    
    # Software Packages
    try:
        software = get_category_by_name("Software Packages", "Computer and Tech")
        brands = ["Kaspersky", "Microsoft", "Norton"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Software Packages")
    except Category.DoesNotExist:
        print("⚠️ Software Packages category not found")

def populate_tools_equipment_brands():
    """Populate brands for Tools and Equipment category and subcategories"""
    print("Populating Tools and Equipment brands...")
    
    # Power Drills
    try:
        power_drills = get_category_by_name("Power Drills", "Tools and Equipment")
        brands = ["Bosch", "Black+Decker", "Dewalt"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Power Drills")
    except Category.DoesNotExist:
        print("⚠️ Power Drills category not found")
    
    # Welding Machines
    try:
        welding_machines = get_category_by_name("Welding Machines", "Tools and Equipment")
        brands = ["Rilon", "ESAB", "Panasonic"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Welding Machines")
    except Category.DoesNotExist:
        print("⚠️ Welding Machines category not found")
    
    # Screwdriver Sets
    try:
        screwdriver_sets = get_category_by_name("Screwdriver Sets", "Tools and Equipment")
        brands = ["Stanley", "Bosch", "Taparia"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Screwdriver Sets")
    except Category.DoesNotExist:
        print("⚠️ Screwdriver Sets category not found")
    
    # Measuring Tapes
    try:
        measuring_tapes = get_category_by_name("Measuring Tapes", "Tools and Equipment")
        brands = ["Freemans", "Stanley", "Bosch"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Measuring Tapes")
    except Category.DoesNotExist:
        print("⚠️ Measuring Tapes category not found")
    
    # Air Compressors
    try:
        air_compressors = get_category_by_name("Air Compressors", "Tools and Equipment")
        brands = ["Elgi", "Ingersoll Rand", "Tiger"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Air Compressors")
    except Category.DoesNotExist:
        print("⚠️ Air Compressors category not found")
    
    # Multimeters
    try:
        multimeters = get_category_by_name("Multimeters", "Tools and Equipment")
        brands = ["Meco", "Fluke", "HTC"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Multimeters")
    except Category.DoesNotExist:
        print("⚠️ Multimeters category not found")
    
    # Ladders
    try:
        ladders = get_category_by_name("Ladders", "Tools and Equipment")
        brands = ["Bathla", "Gorilla", "Werner"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Ladders")
    except Category.DoesNotExist:
        print("⚠️ Ladders category not found")
    
    # Angle Grinders
    try:
        angle_grinders = get_category_by_name("Angle Grinders", "Tools and Equipment")
        brands = ["Makita", "Bosch", "Dewalt"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Angle Grinders")
    except Category.DoesNotExist:
        print("⚠️ Angle Grinders category not found")
    
    # Tool Kits
    try:
        tool_kits = get_category_by_name("Tool Kits", "Tools and Equipment")
        brands = ["Taparia", "Stanley", "Black+Decker"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Tool Kits")
    except Category.DoesNotExist:
        print("⚠️ Tool Kits category not found")
    
    # Chainsaws
    try:
        chainsaws = get_category_by_name("Chainsaws", "Tools and Equipment")
        brands = ["Stihl", "Husqvarna", "Makita"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Chainsaws")
    except Category.DoesNotExist:
        print("⚠️ Chainsaws category not found")

def populate_sports_outdoor_brands():
    """Populate brands for Sports and Outdoor category and subcategories"""
    print("Populating Sports and Outdoor brands...")
    
    # Treadmills
    try:
        treadmills = get_category_by_name("Treadmills", "Sports and Outdoor")
        brands = ["PowerMax", "Durafit", "Cockatoo"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Treadmills")
    except Category.DoesNotExist:
        print("⚠️ Treadmills category not found")
    
    # Dumbbell Sets
    try:
        dumbbell_sets = get_category_by_name("Dumbbell Sets", "Sports and Outdoor")
        brands = ["Kobo", "Aurion", "AmazonBasics"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Dumbbell Sets")
    except Category.DoesNotExist:
        print("⚠️ Dumbbell Sets category not found")
    
    # Football Shoes
    try:
        football_shoes = get_category_by_name("Football Shoes", "Sports and Outdoor")
        brands = ["Nike", "Adidas", "Puma"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Football Shoes")
    except Category.DoesNotExist:
        print("⚠️ Football Shoes category not found")
    
    # Bicycles
    try:
        bicycles = get_category_by_name("Bicycles", "Sports and Outdoor")
        brands = ["Hero", "Firefox", "Trek"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Bicycles")
    except Category.DoesNotExist:
        print("⚠️ Bicycles category not found")
    
    # Cricket Bats
    try:
        cricket_bats = get_category_by_name("Cricket Bats", "Sports and Outdoor")
        brands = ["SS", "SG", "Kookaburra"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Cricket Bats")
    except Category.DoesNotExist:
        print("⚠️ Cricket Bats category not found")
    
    # Camping Tents
    try:
        camping_tents = get_category_by_name("Camping Tents", "Sports and Outdoor")
        brands = ["Quechua", "Coleman", "Wildcraft"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Camping Tents")
    except Category.DoesNotExist:
        print("⚠️ Camping Tents category not found")
    
    # Yoga Mats
    try:
        yoga_mats = get_category_by_name("Yoga Mats", "Sports and Outdoor")
        brands = ["AmazonBasics", "Boldfit", "Adidas"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Yoga Mats")
    except Category.DoesNotExist:
        print("⚠️ Yoga Mats category not found")
    
    # Skates
    try:
        skates = get_category_by_name("Skates", "Sports and Outdoor")
        brands = ["Nivia", "Cosco", "Rollerblade"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Skates")
    except Category.DoesNotExist:
        print("⚠️ Skates category not found")
    
    # Badminton Rackets
    try:
        badminton_rackets = get_category_by_name("Badminton Rackets", "Sports and Outdoor")
        brands = ["Yonex", "Li-Ning", "Carlton"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Badminton Rackets")
    except Category.DoesNotExist:
        print("⚠️ Badminton Rackets category not found")
    
    # Boxing Gloves
    try:
        boxing_gloves = get_category_by_name("Boxing Gloves", "Sports and Outdoor")
        brands = ["Everlast", "USI", "Adidas"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Boxing Gloves")
    except Category.DoesNotExist:
        print("⚠️ Boxing Gloves category not found")

def populate_animals_pets_brands():
    """Populate brands for Animals and Pets category and subcategories"""
    print("Populating Animals and Pets brands...")
    
    # Dog Food
    try:
        dog_food = get_category_by_name("Dog Food", "Animals and Pets")
        brands = ["Pedigree", "Drools", "Royal Canin"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Dog Food")
    except Category.DoesNotExist:
        print("⚠️ Dog Food category not found")
    
    # Cat Litter
    try:
        cat_litter = get_category_by_name("Cat Litter", "Animals and Pets")
        brands = ["Kit Cat", "Ever Clean", "Me-O"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Cat Litter")
    except Category.DoesNotExist:
        print("⚠️ Cat Litter category not found")
    
    # Bird Cages
    try:
        bird_cages = get_category_by_name("Bird Cages", "Animals and Pets")
        brands = ["Savic", "Prevue", "Yaheetech"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Bird Cages")
    except Category.DoesNotExist:
        print("⚠️ Bird Cages category not found")
    
    # Fish Tanks
    try:
        fish_tanks = get_category_by_name("Fish Tanks", "Animals and Pets")
        brands = ["Boyu", "Sobo", "Marina"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Fish Tanks")
    except Category.DoesNotExist:
        print("⚠️ Fish Tanks category not found")
    
    # Pet Toys
    try:
        pet_toys = get_category_by_name("Pet Toys", "Animals and Pets")
        brands = ["KONG", "BarkBox", "Trixie"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Pet Toys")
    except Category.DoesNotExist:
        print("⚠️ Pet Toys category not found")
    
    # Leashes
    try:
        leashes = get_category_by_name("Leashes", "Animals and Pets")
        brands = ["PetSafe", "Trixie", "Fida"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Leashes")
    except Category.DoesNotExist:
        print("⚠️ Leashes category not found")
    
    # Dog Beds
    try:
        dog_beds = get_category_by_name("Dog Beds", "Animals and Pets")
        brands = ["FurHaven", "MidWest", "AmazonBasics"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Dog Beds")
    except Category.DoesNotExist:
        print("⚠️ Dog Beds category not found")
    
    # Aquarium Accessories
    try:
        aquarium_accessories = get_category_by_name("Aquarium Accessories", "Animals and Pets")
        brands = ["SunSun", "Boyu", "Aquael"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Aquarium Accessories")
    except Category.DoesNotExist:
        print("⚠️ Aquarium Accessories category not found")
    
    # Pet Grooming Kits
    try:
        grooming_kits = get_category_by_name("Pet Grooming Kits", "Animals and Pets")
        brands = ["Wahl", "Petology", "Andis"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Pet Grooming Kits")
    except Category.DoesNotExist:
        print("⚠️ Pet Grooming Kits category not found")
    
    # Pet Carriers
    try:
        pet_carriers = get_category_by_name("Pet Carriers", "Animals and Pets")
        brands = ["Petmate", "AmazonBasics", "Ferplast"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Pet Carriers")
    except Category.DoesNotExist:
        print("⚠️ Pet Carriers category not found")

def populate_machinery_tools_brands():
    """Populate brands for Machinery Tools category and subcategories"""
    print("Populating Machinery Tools brands...")
    
    # Industrial Generators
    try:
        industrial_generators = get_category_by_name("Industrial Generators", "Machinery Tools")
        brands = ["Kirloskar", "Cummins", "Honda"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Industrial Generators")
    except Category.DoesNotExist:
        print("⚠️ Industrial Generators category not found")
    
    # CNC Machines
    try:
        cnc_machines = get_category_by_name("CNC Machines", "Machinery Tools")
        brands = ["Haas", "Siemens", "Mazak"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for CNC Machines")
    except Category.DoesNotExist:
        print("⚠️ CNC Machines category not found")
    
    # Hydraulic Presses
    try:
        hydraulic_presses = get_category_by_name("Hydraulic Presses", "Machinery Tools")
        brands = ["Enerpac", "Dake", "Baileigh"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Hydraulic Presses")
    except Category.DoesNotExist:
        print("⚠️ Hydraulic Presses category not found")
    
    # Lathe Machines
    try:
        lathe_machines = get_category_by_name("Lathe Machines", "Machinery Tools")
        brands = ["HMT", "ACE", "Bhavya"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Lathe Machines")
    except Category.DoesNotExist:
        print("⚠️ Lathe Machines category not found")
    
    # Forklifts
    try:
        forklifts = get_category_by_name("Forklifts", "Machinery Tools")
        brands = ["Toyota", "CAT", "Godrej"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Forklifts")
    except Category.DoesNotExist:
        print("⚠️ Forklifts category not found")
    
    # Air Handling Units
    try:
        air_handling_units = get_category_by_name("Air Handling Units", "Machinery Tools")
        brands = ["Voltas", "Carrier", "Blue Star"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Air Handling Units")
    except Category.DoesNotExist:
        print("⚠️ Air Handling Units category not found")
    
    # Water Pumps
    try:
        water_pumps = get_category_by_name("Water Pumps", "Machinery Tools")
        brands = ["Crompton", "Kirloskar", "Havells"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Water Pumps")
    except Category.DoesNotExist:
        print("⚠️ Water Pumps category not found")
    
    # Industrial Vacuum Cleaners
    try:
        industrial_vacuums = get_category_by_name("Industrial Vacuum Cleaners", "Machinery Tools")
        brands = ["Karcher", "IPC", "Nilfisk"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Industrial Vacuum Cleaners")
    except Category.DoesNotExist:
        print("⚠️ Industrial Vacuum Cleaners category not found")
    
    # Welding Generators
    try:
        welding_generators = get_category_by_name("Welding Generators", "Machinery Tools")
        brands = ["Koike", "Honda", "Lincoln"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Welding Generators")
    except Category.DoesNotExist:
        print("⚠️ Welding Generators category not found")
    
    # Material Handling Cranes
    try:
        material_cranes = get_category_by_name("Material Handling Cranes", "Machinery Tools")
        brands = ["Demag", "Konecranes", "ElectroMech"]
        for brand_name in brands:
            create_brand(brand_name)
        print(f"✓ Added {len(brands)} brands for Material Handling Cranes")
    except Category.DoesNotExist:
        print("⚠️ Material Handling Cranes category not found")

def main():
    """Main function to populate all brands"""
    print("Starting to populate brands for all categories...")
    print("=" * 50)
    
    # Populate brands for all categories
    populate_electronics_brands()
    print()
    
    populate_automobiles_brands()
    print()
    
    populate_clothing_brands()
    print()
    
    populate_home_interiors_brands()
    print()
    
    populate_computer_tech_brands()
    print()
    
    populate_tools_equipment_brands()
    print()
    
    populate_sports_outdoor_brands()
    print()
    
    populate_animals_pets_brands()
    print()
    
    populate_machinery_tools_brands()
    print()
    
    # Print summary
    total_brands = Brand.objects.count()
    print("=" * 50)
    print(f"✅ Brand population completed successfully!")
    print(f"📊 Total brands in database: {total_brands}")
    print("=" * 50)

if __name__ == "__main__":
    main() 