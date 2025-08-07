#!/usr/bin/env python
"""
Script to populate categories and attributes for MarketVibe
Run this script from the Django project root directory
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketVibe.settings')
django.setup()

from seller.models import Category, CategoryAttribute, AttributeOption, InputType

def create_category(name, parent=None, description=None):
    """Create a category if it doesn't exist"""
    category, created = Category.objects.get_or_create(
        name=name,
        defaults={'parent': parent, 'description': description}
    )
    return category

def create_attribute(category, name, input_type, unit=None, is_required=False):
    """Create a category attribute"""
    attr, created = CategoryAttribute.objects.get_or_create(
        category=category,
        name=name,
        defaults={
            'input_type': input_type,
            'unit': unit,
            'is_required': is_required
        }
    )
    return attr

def create_attribute_options(attribute, options):
    """Create options for dropdown attributes"""
    for option in options:
        AttributeOption.objects.get_or_create(
            attribute=attribute,
            value=option
        )

def populate_electronics():
    """Populate Electronics category and subcategories"""
    electronics = create_category("Electronics")
    
    # Smartphones
    smartphones = create_category("Smartphones", electronics)
    
    # Brand attribute
    brand_attr = create_attribute(smartphones, "Brand", InputType.DROPDOWN)
    create_attribute_options(brand_attr, ["Apple", "Samsung", "Xiaomi", "Oppo"])
    
    # RAM attribute
    ram_attr = create_attribute(smartphones, "RAM", InputType.DROPDOWN, "GB")
    create_attribute_options(ram_attr, ["4", "6", "8", "12"])
    
    # Storage attribute
    storage_attr = create_attribute(smartphones, "Storage", InputType.DROPDOWN, "GB")
    create_attribute_options(storage_attr, ["64", "128", "256", "512"])
    
    # Battery Capacity
    create_attribute(smartphones, "Battery Capacity", InputType.NUMBER, "mAh")
    
    # 5G Support
    g5_attr = create_attribute(smartphones, "5G Support", InputType.BOOLEAN)
    create_attribute_options(g5_attr, ["Yes", "No"])
    
    # Laptops
    laptops = create_category("Laptops", electronics)
    
    # Processor
    processor_attr = create_attribute(laptops, "Processor", InputType.DROPDOWN)
    create_attribute_options(processor_attr, ["Intel i5", "i7", "Ryzen 5", "Ryzen 7"])
    
    # RAM
    laptop_ram_attr = create_attribute(laptops, "RAM", InputType.DROPDOWN, "GB")
    create_attribute_options(laptop_ram_attr, ["8", "16", "32"])
    
    # SSD Size
    ssd_attr = create_attribute(laptops, "SSD Size", InputType.DROPDOWN, "GB")
    create_attribute_options(ssd_attr, ["256", "512", "1024"])
    
    # Graphics Card
    create_attribute(laptops, "Graphics Card", InputType.TEXT)
    
    # Screen Size
    create_attribute(laptops, "Screen Size", InputType.NUMBER, "inches")
    
    # Smart Watches
    smartwatches = create_category("Smart Watches", electronics)
    
    # Brand
    watch_brand_attr = create_attribute(smartwatches, "Brand", InputType.DROPDOWN)
    create_attribute_options(watch_brand_attr, ["Apple", "Samsung", "Fitbit", "Xiaomi"])
    
    # Strap Material
    strap_attr = create_attribute(smartwatches, "Strap Material", InputType.DROPDOWN)
    create_attribute_options(strap_attr, ["Silicone", "Leather", "Metal"])
    
    # Waterproof
    waterproof_attr = create_attribute(smartwatches, "Waterproof", InputType.BOOLEAN)
    create_attribute_options(waterproof_attr, ["Yes", "No"])
    
    # Battery Life
    create_attribute(smartwatches, "Battery Life", InputType.NUMBER, "hours")
    
    # LED TVs
    led_tvs = create_category("LED TVs", electronics)
    
    # Screen Size
    create_attribute(led_tvs, "Screen Size", InputType.NUMBER, "inches")
    
    # Resolution
    resolution_attr = create_attribute(led_tvs, "Resolution", InputType.DROPDOWN)
    create_attribute_options(resolution_attr, ["HD", "Full HD", "4K", "8K"])
    
    # Smart TV
    smart_tv_attr = create_attribute(led_tvs, "Smart TV", InputType.BOOLEAN)
    create_attribute_options(smart_tv_attr, ["Yes", "No"])
    
    # HDMI Ports
    create_attribute(led_tvs, "HDMI Ports", InputType.NUMBER)
    
    # Bluetooth Speakers
    bluetooth_speakers = create_category("Bluetooth Speakers", electronics)
    
    # Brand
    speaker_brand_attr = create_attribute(bluetooth_speakers, "Brand", InputType.DROPDOWN)
    create_attribute_options(speaker_brand_attr, ["JBL", "Bose", "Sony", "Anker"])
    
    # Battery Life
    create_attribute(bluetooth_speakers, "Battery Life", InputType.NUMBER, "hours")
    
    # Waterproof
    speaker_waterproof_attr = create_attribute(bluetooth_speakers, "Waterproof", InputType.BOOLEAN)
    create_attribute_options(speaker_waterproof_attr, ["Yes", "No"])
    
    # Bluetooth Version
    bt_version_attr = create_attribute(bluetooth_speakers, "Bluetooth Version", InputType.DROPDOWN)
    create_attribute_options(bt_version_attr, ["4.0", "4.2", "5.0", "5.3"])
    
    # Cameras
    cameras = create_category("Cameras", electronics)
    
    # Type
    camera_type_attr = create_attribute(cameras, "Type", InputType.DROPDOWN)
    create_attribute_options(camera_type_attr, ["DSLR", "Mirrorless", "Point & Shoot"])
    
    # Megapixels
    create_attribute(cameras, "Megapixels", InputType.NUMBER, "MP")
    
    # Lens Mount
    create_attribute(cameras, "Lens Mount", InputType.TEXT)
    
    # 4K Video
    video_attr = create_attribute(cameras, "4K Video", InputType.BOOLEAN)
    create_attribute_options(video_attr, ["Yes", "No"])
    
    # Headphones
    headphones = create_category("Headphones", electronics)
    
    # Type
    headphone_type_attr = create_attribute(headphones, "Type", InputType.DROPDOWN)
    create_attribute_options(headphone_type_attr, ["Over-ear", "In-ear", "On-ear"])
    
    # Noise Cancellation
    noise_attr = create_attribute(headphones, "Noise Cancellation", InputType.BOOLEAN)
    create_attribute_options(noise_attr, ["Yes", "No"])
    
    # Wired/Wireless
    connection_attr = create_attribute(headphones, "Wired/Wireless", InputType.DROPDOWN)
    create_attribute_options(connection_attr, ["Wired", "Wireless"])
    
    # Power Banks
    power_banks = create_category("Power Banks", electronics)
    
    # Capacity
    create_attribute(power_banks, "Capacity", InputType.NUMBER, "mAh")
    
    # Fast Charging
    fast_charge_attr = create_attribute(power_banks, "Fast Charging", InputType.BOOLEAN)
    create_attribute_options(fast_charge_attr, ["Yes", "No"])
    
    # USB Ports
    create_attribute(power_banks, "USB Ports", InputType.NUMBER)
    
    # Gaming Consoles
    gaming_consoles = create_category("Gaming Consoles", electronics)
    
    # Brand
    console_brand_attr = create_attribute(gaming_consoles, "Brand", InputType.DROPDOWN)
    create_attribute_options(console_brand_attr, ["Sony", "Microsoft", "Nintendo"])
    
    # Storage
    console_storage_attr = create_attribute(gaming_consoles, "Storage", InputType.DROPDOWN, "GB")
    create_attribute_options(console_storage_attr, ["512", "1000"])
    
    # Controllers Included
    create_attribute(gaming_consoles, "Controllers Included", InputType.NUMBER)
    
    # Drones
    drones = create_category("Drones", electronics)
    
    # Flight Time
    create_attribute(drones, "Flight Time", InputType.NUMBER, "minutes")
    
    # Camera Resolution
    create_attribute(drones, "Camera Resolution", InputType.NUMBER, "MP")
    
    # Max Range
    create_attribute(drones, "Max Range", InputType.NUMBER, "meters")
    
    # GPS Enabled
    gps_attr = create_attribute(drones, "GPS Enabled", InputType.BOOLEAN)
    create_attribute_options(gps_attr, ["Yes", "No"])

def populate_automobiles():
    """Populate Automobiles category and subcategories"""
    automobiles = create_category("Automobiles")
    
    # Cars
    cars = create_category("Cars", automobiles)
    
    # Brand
    car_brand_attr = create_attribute(cars, "Brand", InputType.DROPDOWN)
    create_attribute_options(car_brand_attr, ["Toyota", "Honda", "Kia", "Hyundai"])
    
    # Fuel Type
    fuel_attr = create_attribute(cars, "Fuel Type", InputType.DROPDOWN)
    create_attribute_options(fuel_attr, ["Petrol", "Diesel", "Hybrid", "Electric"])
    
    # Transmission
    transmission_attr = create_attribute(cars, "Transmission", InputType.DROPDOWN)
    create_attribute_options(transmission_attr, ["Manual", "Automatic"])
    
    # Engine Capacity
    create_attribute(cars, "Engine Capacity", InputType.NUMBER, "cc")
    
    # Bikes
    bikes = create_category("Bikes", automobiles)
    
    # Engine CC
    create_attribute(bikes, "Engine CC", InputType.NUMBER, "cc")
    
    # Type
    bike_type_attr = create_attribute(bikes, "Type", InputType.DROPDOWN)
    create_attribute_options(bike_type_attr, ["Sports", "Cruiser", "Commuter"])
    
    # ABS
    abs_attr = create_attribute(bikes, "ABS", InputType.BOOLEAN)
    create_attribute_options(abs_attr, ["Yes", "No"])
    
    # Electric Scooters
    e_scooters = create_category("Electric Scooters", automobiles)
    
    # Battery Range
    create_attribute(e_scooters, "Battery Range", InputType.NUMBER, "km")
    
    # Charging Time
    create_attribute(e_scooters, "Charging Time", InputType.NUMBER, "hours")
    
    # Top Speed
    create_attribute(e_scooters, "Top Speed", InputType.NUMBER, "km/h")
    
    # Car Accessories
    car_accessories = create_category("Car Accessories", automobiles)
    
    # Type
    accessory_type_attr = create_attribute(car_accessories, "Type", InputType.DROPDOWN)
    create_attribute_options(accessory_type_attr, ["Cover", "Wipers", "Air Freshener", "Mats"])
    
    # Universal Fit
    universal_attr = create_attribute(car_accessories, "Universal Fit", InputType.BOOLEAN)
    create_attribute_options(universal_attr, ["Yes", "No"])
    
    # Tyres
    tyres = create_category("Tyres", automobiles)
    
    # Diameter
    create_attribute(tyres, "Diameter", InputType.NUMBER, "inches")
    
    # Type
    tyre_type_attr = create_attribute(tyres, "Type", InputType.DROPDOWN)
    create_attribute_options(tyre_type_attr, ["Tubeless", "Tube"])
    
    # Brand
    tyre_brand_attr = create_attribute(tyres, "Brand", InputType.DROPDOWN)
    create_attribute_options(tyre_brand_attr, ["Michelin", "Yokohama", "Dunlop"])
    
    # Car Batteries
    car_batteries = create_category("Car Batteries", automobiles)
    
    # Voltage
    create_attribute(car_batteries, "Voltage", InputType.NUMBER, "V")
    
    # Capacity
    create_attribute(car_batteries, "Capacity", InputType.NUMBER, "Ah")
    
    # Warranty
    warranty_attr = create_attribute(car_batteries, "Warranty", InputType.DROPDOWN)
    create_attribute_options(warranty_attr, ["6 Months", "12 Months", "18 Months"])
    
    # Motorbike Helmets
    helmets = create_category("Motorbike Helmets", automobiles)
    
    # Size
    helmet_size_attr = create_attribute(helmets, "Size", InputType.DROPDOWN)
    create_attribute_options(helmet_size_attr, ["S", "M", "L", "XL"])
    
    # Material
    helmet_material_attr = create_attribute(helmets, "Material", InputType.DROPDOWN)
    create_attribute_options(helmet_material_attr, ["ABS", "Fiberglass", "Carbon Fiber"])
    
    # ISI Certified
    isi_attr = create_attribute(helmets, "ISI Certified", InputType.BOOLEAN)
    create_attribute_options(isi_attr, ["Yes", "No"])
    
    # Car Audio Systems
    car_audio = create_category("Car Audio Systems", automobiles)
    
    # Output Power
    create_attribute(car_audio, "Output Power", InputType.NUMBER, "watts")
    
    # Bluetooth Enabled
    bt_enabled_attr = create_attribute(car_audio, "Bluetooth Enabled", InputType.BOOLEAN)
    create_attribute_options(bt_enabled_attr, ["Yes", "No"])
    
    # Display Type
    display_attr = create_attribute(car_audio, "Display Type", InputType.DROPDOWN)
    create_attribute_options(display_attr, ["LED", "LCD"])
    
    # Truck Parts
    truck_parts = create_category("Truck Parts", automobiles)
    
    # Part Type
    create_attribute(truck_parts, "Part Type", InputType.TEXT)
    
    # Compatibility
    create_attribute(truck_parts, "Compatibility", InputType.TEXT)
    
    # Brand
    create_attribute(truck_parts, "Brand", InputType.TEXT)
    
    # SUV Accessories
    suv_accessories = create_category("SUV Accessories", automobiles)
    
    # Roof Rack
    roof_rack_attr = create_attribute(suv_accessories, "Roof Rack", InputType.BOOLEAN)
    create_attribute_options(roof_rack_attr, ["Yes", "No"])
    
    # Towing Hook
    towing_attr = create_attribute(suv_accessories, "Towing Hook", InputType.BOOLEAN)
    create_attribute_options(towing_attr, ["Yes", "No"])
    
    # Material
    suv_material_attr = create_attribute(suv_accessories, "Material", InputType.DROPDOWN)
    create_attribute_options(suv_material_attr, ["Aluminum", "Steel", "Plastic"])

def populate_clothing():
    """Populate Clothes and Wear category and subcategories"""
    clothing = create_category("Clothes and Wear")
    
    # Men's T-Shirts
    mens_tshirts = create_category("Men's T-Shirts", clothing)
    
    # Brand
    tshirt_brand_attr = create_attribute(mens_tshirts, "Brand", InputType.DROPDOWN)
    create_attribute_options(tshirt_brand_attr, ["Nike", "Adidas", "Levi's", "Uniqlo"])
    
    # Size
    tshirt_size_attr = create_attribute(mens_tshirts, "Size", InputType.DROPDOWN)
    create_attribute_options(tshirt_size_attr, ["S", "M", "L", "XL", "XXL"])
    
    # Material
    tshirt_material_attr = create_attribute(mens_tshirts, "Material", InputType.DROPDOWN)
    create_attribute_options(tshirt_material_attr, ["Cotton", "Polyester", "Blended"])
    
    # Sleeve Type
    sleeve_attr = create_attribute(mens_tshirts, "Sleeve Type", InputType.DROPDOWN)
    create_attribute_options(sleeve_attr, ["Full", "Half", "Sleeveless"])
    
    # Fit
    fit_attr = create_attribute(mens_tshirts, "Fit", InputType.DROPDOWN)
    create_attribute_options(fit_attr, ["Slim", "Regular", "Loose"])
    
    # Women's Dresses
    womens_dresses = create_category("Women's Dresses", clothing)
    
    # Size
    dress_size_attr = create_attribute(womens_dresses, "Size", InputType.DROPDOWN)
    create_attribute_options(dress_size_attr, ["XS", "S", "M", "L", "XL"])
    
    # Material
    dress_material_attr = create_attribute(womens_dresses, "Material", InputType.DROPDOWN)
    create_attribute_options(dress_material_attr, ["Cotton", "Silk", "Rayon"])
    
    # Pattern
    pattern_attr = create_attribute(womens_dresses, "Pattern", InputType.DROPDOWN)
    create_attribute_options(pattern_attr, ["Printed", "Solid", "Embroidered"])
    
    # Length
    length_attr = create_attribute(womens_dresses, "Length", InputType.DROPDOWN)
    create_attribute_options(length_attr, ["Mini", "Midi", "Maxi"])
    
    # Occasion
    occasion_attr = create_attribute(womens_dresses, "Occasion", InputType.DROPDOWN)
    create_attribute_options(occasion_attr, ["Casual", "Formal", "Party"])
    
    # Men's Jeans
    mens_jeans = create_category("Men's Jeans", clothing)
    
    # Waist Size
    create_attribute(mens_jeans, "Waist Size", InputType.NUMBER, "inches")
    
    # Length
    create_attribute(mens_jeans, "Length", InputType.NUMBER, "inches")
    
    # Fit
    jeans_fit_attr = create_attribute(mens_jeans, "Fit", InputType.DROPDOWN)
    create_attribute_options(jeans_fit_attr, ["Slim", "Skinny", "Regular", "Relaxed"])
    
    # Wash
    wash_attr = create_attribute(mens_jeans, "Wash", InputType.DROPDOWN)
    create_attribute_options(wash_attr, ["Light", "Medium", "Dark"])
    
    # Women's Tops
    womens_tops = create_category("Women's Tops", clothing)
    
    # Size
    top_size_attr = create_attribute(womens_tops, "Size", InputType.DROPDOWN)
    create_attribute_options(top_size_attr, ["XS", "S", "M", "L", "XL"])
    
    # Neck Type
    neck_attr = create_attribute(womens_tops, "Neck Type", InputType.DROPDOWN)
    create_attribute_options(neck_attr, ["Round", "V-neck", "Collar", "Boat"])
    
    # Sleeve Length
    sleeve_length_attr = create_attribute(womens_tops, "Sleeve Length", InputType.DROPDOWN)
    create_attribute_options(sleeve_length_attr, ["Full", "Half", "3/4th", "Sleeveless"])
    
    # Children's Clothing
    children_clothing = create_category("Children's Clothing", clothing)
    
    # Age Group
    age_attr = create_attribute(children_clothing, "Age Group", InputType.DROPDOWN)
    create_attribute_options(age_attr, ["0-1", "1-3", "3-5", "5-7", "7-10"])
    
    # Gender
    gender_attr = create_attribute(children_clothing, "Gender", InputType.DROPDOWN)
    create_attribute_options(gender_attr, ["Boys", "Girls", "Unisex"])
    
    # Material
    child_material_attr = create_attribute(children_clothing, "Material", InputType.DROPDOWN)
    create_attribute_options(child_material_attr, ["Cotton", "Wool", "Fleece"])
    
    # Footwear
    footwear = create_category("Footwear", clothing)
    
    # Size
    create_attribute(footwear, "Size", InputType.NUMBER)
    
    # Brand
    shoe_brand_attr = create_attribute(footwear, "Brand", InputType.DROPDOWN)
    create_attribute_options(shoe_brand_attr, ["Nike", "Adidas", "Skechers", "Bata"])
    
    # Type
    shoe_type_attr = create_attribute(footwear, "Type", InputType.DROPDOWN)
    create_attribute_options(shoe_type_attr, ["Sneakers", "Boots", "Sandals", "Formal"])
    
    # Sole Material
    sole_attr = create_attribute(footwear, "Sole Material", InputType.DROPDOWN)
    create_attribute_options(sole_attr, ["Rubber", "EVA", "PU"])
    
    # Winter Jackets
    winter_jackets = create_category("Winter Jackets", clothing)
    
    # Size
    jacket_size_attr = create_attribute(winter_jackets, "Size", InputType.DROPDOWN)
    create_attribute_options(jacket_size_attr, ["S", "M", "L", "XL"])
    
    # Material
    jacket_material_attr = create_attribute(winter_jackets, "Material", InputType.DROPDOWN)
    create_attribute_options(jacket_material_attr, ["Wool", "Polyester", "Fleece"])
    
    # Waterproof
    jacket_waterproof_attr = create_attribute(winter_jackets, "Waterproof", InputType.BOOLEAN)
    create_attribute_options(jacket_waterproof_attr, ["Yes", "No"])
    
    # Hooded
    hooded_attr = create_attribute(winter_jackets, "Hooded", InputType.BOOLEAN)
    create_attribute_options(hooded_attr, ["Yes", "No"])
    
    # Socks
    socks = create_category("Socks", clothing)
    
    # Size
    sock_size_attr = create_attribute(socks, "Size", InputType.DROPDOWN)
    create_attribute_options(sock_size_attr, ["Free Size", "S", "M", "L"])
    
    # Fabric
    sock_fabric_attr = create_attribute(socks, "Fabric", InputType.DROPDOWN)
    create_attribute_options(sock_fabric_attr, ["Cotton", "Wool", "Nylon"])
    
    # Length
    sock_length_attr = create_attribute(socks, "Length", InputType.DROPDOWN)
    create_attribute_options(sock_length_attr, ["Ankle", "Crew", "Calf", "Knee"])
    
    # Caps and Hats
    caps_hats = create_category("Caps and Hats", clothing)
    
    # Type
    hat_type_attr = create_attribute(caps_hats, "Type", InputType.DROPDOWN)
    create_attribute_options(hat_type_attr, ["Baseball", "Fedora", "Beanie", "Bucket"])
    
    # Material
    hat_material_attr = create_attribute(caps_hats, "Material", InputType.DROPDOWN)
    create_attribute_options(hat_material_attr, ["Cotton", "Wool", "Polyester"])
    
    # Adjustable Strap
    adjustable_attr = create_attribute(caps_hats, "Adjustable Strap", InputType.BOOLEAN)
    create_attribute_options(adjustable_attr, ["Yes", "No"])
    
    # Belts
    belts = create_category("Belts", clothing)
    
    # Waist Size
    create_attribute(belts, "Waist Size", InputType.NUMBER, "inches")
    
    # Material
    belt_material_attr = create_attribute(belts, "Material", InputType.DROPDOWN)
    create_attribute_options(belt_material_attr, ["Leather", "PU", "Canvas"])
    
    # Buckle Type
    buckle_attr = create_attribute(belts, "Buckle Type", InputType.DROPDOWN)
    create_attribute_options(buckle_attr, ["Pin", "Automatic", "Reversible"])

def main():
    """Main function to populate all categories and attributes"""
    print("Starting to populate categories and attributes...")
    
    # Populate Electronics
    print("Populating Electronics...")
    populate_electronics()
    
    # Populate Automobiles
    print("Populating Automobiles...")
    populate_automobiles()
    
    # Populate Clothing
    print("Populating Clothing...")
    populate_clothing()
    
    print("Categories and attributes populated successfully!")

if __name__ == "__main__":
    main() 