#!/usr/bin/env python
"""
Script to populate remaining categories and attributes for MarketVibe
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

def populate_home_interiors():
    """Populate Home Interiors category and subcategories"""
    home_interiors = create_category("Home Interiors")
    
    # Sofas
    sofas = create_category("Sofas", home_interiors)
    
    # Seating Capacity
    seating_attr = create_attribute(sofas, "Seating Capacity", InputType.DROPDOWN)
    create_attribute_options(seating_attr, ["2", "3", "4", "5"])
    
    # Material
    sofa_material_attr = create_attribute(sofas, "Material", InputType.DROPDOWN)
    create_attribute_options(sofa_material_attr, ["Leather", "Fabric", "Velvet"])
    
    # Color
    create_attribute(sofas, "Color", InputType.TEXT)
    
    # Recliner
    recliner_attr = create_attribute(sofas, "Recliner", InputType.BOOLEAN)
    create_attribute_options(recliner_attr, ["Yes", "No"])
    
    # Beds
    beds = create_category("Beds", home_interiors)
    
    # Size
    bed_size_attr = create_attribute(beds, "Size", InputType.DROPDOWN)
    create_attribute_options(bed_size_attr, ["Single", "Double", "Queen", "King"])
    
    # Storage Included
    storage_attr = create_attribute(beds, "Storage Included", InputType.BOOLEAN)
    create_attribute_options(storage_attr, ["Yes", "No"])
    
    # Frame Material
    frame_material_attr = create_attribute(beds, "Frame Material", InputType.DROPDOWN)
    create_attribute_options(frame_material_attr, ["Wood", "Metal", "MDF"])
    
    # Curtains
    curtains = create_category("Curtains", home_interiors)
    
    # Length
    create_attribute(curtains, "Length", InputType.NUMBER, "inches")
    
    # Fabric
    curtain_fabric_attr = create_attribute(curtains, "Fabric", InputType.DROPDOWN)
    create_attribute_options(curtain_fabric_attr, ["Cotton", "Linen", "Polyester"])
    
    # Pattern
    curtain_pattern_attr = create_attribute(curtains, "Pattern", InputType.DROPDOWN)
    create_attribute_options(curtain_pattern_attr, ["Plain", "Floral", "Geometric"])
    
    # Wall Clocks
    wall_clocks = create_category("Wall Clocks", home_interiors)
    
    # Diameter
    create_attribute(wall_clocks, "Diameter", InputType.NUMBER, "inches")
    
    # Style
    clock_style_attr = create_attribute(wall_clocks, "Style", InputType.DROPDOWN)
    create_attribute_options(clock_style_attr, ["Modern", "Vintage", "Minimalist"])
    
    # Material
    clock_material_attr = create_attribute(wall_clocks, "Material", InputType.DROPDOWN)
    create_attribute_options(clock_material_attr, ["Plastic", "Metal", "Wood"])
    
    # Ceiling Lights
    ceiling_lights = create_category("Ceiling Lights", home_interiors)
    
    # Type
    light_type_attr = create_attribute(ceiling_lights, "Type", InputType.DROPDOWN)
    create_attribute_options(light_type_attr, ["Chandelier", "Pendant", "Flush Mount"])
    
    # Light Source
    light_source_attr = create_attribute(ceiling_lights, "Light Source", InputType.DROPDOWN)
    create_attribute_options(light_source_attr, ["LED", "CFL", "Halogen"])
    
    # Wattage
    create_attribute(ceiling_lights, "Wattage", InputType.NUMBER, "W")
    
    # Dining Tables
    dining_tables = create_category("Dining Tables", home_interiors)
    
    # Shape
    table_shape_attr = create_attribute(dining_tables, "Shape", InputType.DROPDOWN)
    create_attribute_options(table_shape_attr, ["Rectangular", "Round", "Square"])
    
    # Seats
    seats_attr = create_attribute(dining_tables, "Seats", InputType.DROPDOWN)
    create_attribute_options(seats_attr, ["2", "4", "6", "8"])
    
    # Material
    table_material_attr = create_attribute(dining_tables, "Material", InputType.DROPDOWN)
    create_attribute_options(table_material_attr, ["Wood", "Glass", "Marble"])
    
    # Rugs
    rugs = create_category("Rugs", home_interiors)
    
    # Size
    create_attribute(rugs, "Size", InputType.TEXT)
    
    # Material
    rug_material_attr = create_attribute(rugs, "Material", InputType.DROPDOWN)
    create_attribute_options(rug_material_attr, ["Wool", "Nylon", "Polyester"])
    
    # Pattern
    rug_pattern_attr = create_attribute(rugs, "Pattern", InputType.DROPDOWN)
    create_attribute_options(rug_pattern_attr, ["Solid", "Printed", "Abstract"])
    
    # Storage Cabinets
    storage_cabinets = create_category("Storage Cabinets", home_interiors)
    
    # Number of Shelves
    create_attribute(storage_cabinets, "Number of Shelves", InputType.NUMBER)
    
    # Material
    cabinet_material_attr = create_attribute(storage_cabinets, "Material", InputType.DROPDOWN)
    create_attribute_options(cabinet_material_attr, ["Wood", "Plastic", "MDF"])
    
    # Lockable
    lockable_attr = create_attribute(storage_cabinets, "Lockable", InputType.BOOLEAN)
    create_attribute_options(lockable_attr, ["Yes", "No"])
    
    # Wall Art
    wall_art = create_category("Wall Art", home_interiors)
    
    # Type
    art_type_attr = create_attribute(wall_art, "Type", InputType.DROPDOWN)
    create_attribute_options(art_type_attr, ["Canvas", "Metal", "Acrylic"])
    
    # Dimensions
    create_attribute(wall_art, "Dimensions", InputType.TEXT)
    
    # Framed
    framed_attr = create_attribute(wall_art, "Framed", InputType.BOOLEAN)
    create_attribute_options(framed_attr, ["Yes", "No"])
    
    # Lamps
    lamps = create_category("Lamps", home_interiors)
    
    # Type
    lamp_type_attr = create_attribute(lamps, "Type", InputType.DROPDOWN)
    create_attribute_options(lamp_type_attr, ["Table", "Floor", "Wall-mounted"])
    
    # Light Type
    lamp_light_attr = create_attribute(lamps, "Light Type", InputType.DROPDOWN)
    create_attribute_options(lamp_light_attr, ["LED", "Halogen", "CFL"])
    
    # Adjustable
    adjustable_attr = create_attribute(lamps, "Adjustable", InputType.BOOLEAN)
    create_attribute_options(adjustable_attr, ["Yes", "No"])

def populate_computer_tech():
    """Populate Computer and Tech category and subcategories"""
    computer_tech = create_category("Computer and Tech")
    
    # Desktops
    desktops = create_category("Desktops", computer_tech)
    
    # Processor
    desktop_processor_attr = create_attribute(desktops, "Processor", InputType.DROPDOWN)
    create_attribute_options(desktop_processor_attr, ["Intel i3", "i5", "i7", "Ryzen 5", "Ryzen 7"])
    
    # RAM
    desktop_ram_attr = create_attribute(desktops, "RAM", InputType.DROPDOWN, "GB")
    create_attribute_options(desktop_ram_attr, ["4", "8", "16", "32"])
    
    # Storage Type
    storage_type_attr = create_attribute(desktops, "Storage Type", InputType.DROPDOWN)
    create_attribute_options(storage_type_attr, ["HDD", "SSD", "Hybrid"])
    
    # Graphics Card
    create_attribute(desktops, "Graphics Card", InputType.TEXT)
    
    # Monitors
    monitors = create_category("Monitors", computer_tech)
    
    # Screen Size
    create_attribute(monitors, "Screen Size", InputType.NUMBER, "inches")
    
    # Resolution
    monitor_resolution_attr = create_attribute(monitors, "Resolution", InputType.DROPDOWN)
    create_attribute_options(monitor_resolution_attr, ["Full HD", "2K", "4K"])
    
    # Panel Type
    panel_attr = create_attribute(monitors, "Panel Type", InputType.DROPDOWN)
    create_attribute_options(panel_attr, ["IPS", "TN", "VA"])
    
    # Refresh Rate
    create_attribute(monitors, "Refresh Rate", InputType.NUMBER, "Hz")
    
    # Keyboards
    keyboards = create_category("Keyboards", computer_tech)
    
    # Type
    keyboard_type_attr = create_attribute(keyboards, "Type", InputType.DROPDOWN)
    create_attribute_options(keyboard_type_attr, ["Mechanical", "Membrane"])
    
    # Connection
    keyboard_connection_attr = create_attribute(keyboards, "Connection", InputType.DROPDOWN)
    create_attribute_options(keyboard_connection_attr, ["Wired", "Wireless"])
    
    # Backlit
    backlit_attr = create_attribute(keyboards, "Backlit", InputType.BOOLEAN)
    create_attribute_options(backlit_attr, ["Yes", "No"])
    
    # Mice
    mice = create_category("Mice", computer_tech)
    
    # DPI Range
    dpi_attr = create_attribute(mice, "DPI Range", InputType.DROPDOWN)
    create_attribute_options(dpi_attr, ["800-1600", "1600-3200", "3200-6400"])
    
    # Connection
    mouse_connection_attr = create_attribute(mice, "Connection", InputType.DROPDOWN)
    create_attribute_options(mouse_connection_attr, ["Wired", "Wireless"])
    
    # Programmable Buttons
    create_attribute(mice, "Programmable Buttons", InputType.NUMBER)
    
    # Printers
    printers = create_category("Printers", computer_tech)
    
    # Type
    printer_type_attr = create_attribute(printers, "Type", InputType.DROPDOWN)
    create_attribute_options(printer_type_attr, ["Inkjet", "Laser", "Dot Matrix"])
    
    # Function
    printer_function_attr = create_attribute(printers, "Function", InputType.DROPDOWN)
    create_attribute_options(printer_function_attr, ["Print", "Print + Scan", "All-in-One"])
    
    # Color Printing
    color_print_attr = create_attribute(printers, "Color Printing", InputType.BOOLEAN)
    create_attribute_options(color_print_attr, ["Yes", "No"])
    
    # Routers
    routers = create_category("Routers", computer_tech)
    
    # WiFi Band
    wifi_band_attr = create_attribute(routers, "WiFi Band", InputType.DROPDOWN)
    create_attribute_options(wifi_band_attr, ["Single", "Dual", "Tri-band"])
    
    # Max Speed
    create_attribute(routers, "Max Speed", InputType.NUMBER, "Mbps")
    
    # Ports
    create_attribute(routers, "Ports", InputType.NUMBER)
    
    # External Hard Drives
    external_hdds = create_category("External Hard Drives", computer_tech)
    
    # Storage Capacity
    hdd_capacity_attr = create_attribute(external_hdds, "Storage Capacity", InputType.DROPDOWN, "GB/TB")
    create_attribute_options(hdd_capacity_attr, ["500GB", "1TB", "2TB", "4TB"])
    
    # Connection Type
    hdd_connection_attr = create_attribute(external_hdds, "Connection Type", InputType.DROPDOWN)
    create_attribute_options(hdd_connection_attr, ["USB 2.0", "3.0", "Type-C"])
    
    # Webcams
    webcams = create_category("Webcams", computer_tech)
    
    # Resolution
    webcam_resolution_attr = create_attribute(webcams, "Resolution", InputType.DROPDOWN)
    create_attribute_options(webcam_resolution_attr, ["720p", "1080p", "2K", "4K"])
    
    # Microphone Included
    mic_attr = create_attribute(webcams, "Microphone Included", InputType.BOOLEAN)
    create_attribute_options(mic_attr, ["Yes", "No"])
    
    # Mount Type
    mount_attr = create_attribute(webcams, "Mount Type", InputType.DROPDOWN)
    create_attribute_options(mount_attr, ["Clip-on", "Tripod"])
    
    # Computer Speakers
    computer_speakers = create_category("Computer Speakers", computer_tech)
    
    # Output Power
    create_attribute(computer_speakers, "Output Power", InputType.NUMBER, "watts")
    
    # Channel Configuration
    channel_attr = create_attribute(computer_speakers, "Channel Configuration", InputType.DROPDOWN)
    create_attribute_options(channel_attr, ["2.0", "2.1", "5.1"])
    
    # Bluetooth
    speaker_bt_attr = create_attribute(computer_speakers, "Bluetooth", InputType.BOOLEAN)
    create_attribute_options(speaker_bt_attr, ["Yes", "No"])
    
    # Software Packages
    software = create_category("Software Packages", computer_tech)
    
    # Type
    software_type_attr = create_attribute(software, "Type", InputType.DROPDOWN)
    create_attribute_options(software_type_attr, ["Antivirus", "Office Suite", "OS", "Development"])
    
    # License Duration
    license_attr = create_attribute(software, "License Duration", InputType.DROPDOWN)
    create_attribute_options(license_attr, ["1 Year", "3 Years", "Lifetime"])
    
    # Platform
    platform_attr = create_attribute(software, "Platform", InputType.DROPDOWN)
    create_attribute_options(platform_attr, ["Windows", "Mac", "Linux"])

def populate_tools_equipment():
    """Populate Tools and Equipment category and subcategories"""
    tools_equipment = create_category("Tools and Equipment")
    
    # Power Drills
    power_drills = create_category("Power Drills", tools_equipment)
    
    # Type
    drill_type_attr = create_attribute(power_drills, "Type", InputType.DROPDOWN)
    create_attribute_options(drill_type_attr, ["Corded", "Cordless"])
    
    # Voltage
    create_attribute(power_drills, "Voltage", InputType.NUMBER, "V")
    
    # Chuck Size
    create_attribute(power_drills, "Chuck Size", InputType.NUMBER, "mm")
    
    # Welding Machines
    welding_machines = create_category("Welding Machines", tools_equipment)
    
    # Type
    welding_type_attr = create_attribute(welding_machines, "Type", InputType.DROPDOWN)
    create_attribute_options(welding_type_attr, ["MIG", "TIG", "Arc"])
    
    # Output Current
    create_attribute(welding_machines, "Output Current", InputType.NUMBER, "Amps")
    
    # Input Voltage
    create_attribute(welding_machines, "Input Voltage", InputType.NUMBER, "V")
    
    # Screwdriver Sets
    screwdriver_sets = create_category("Screwdriver Sets", tools_equipment)
    
    # Number of Pieces
    create_attribute(screwdriver_sets, "Number of Pieces", InputType.NUMBER)
    
    # Magnetic Tip
    magnetic_attr = create_attribute(screwdriver_sets, "Magnetic Tip", InputType.BOOLEAN)
    create_attribute_options(magnetic_attr, ["Yes", "No"])
    
    # Material
    screwdriver_material_attr = create_attribute(screwdriver_sets, "Material", InputType.DROPDOWN)
    create_attribute_options(screwdriver_material_attr, ["Steel", "Chrome Vanadium"])
    
    # Measuring Tapes
    measuring_tapes = create_category("Measuring Tapes", tools_equipment)
    
    # Length
    create_attribute(measuring_tapes, "Length", InputType.NUMBER, "meters")
    
    # Blade Material
    blade_material_attr = create_attribute(measuring_tapes, "Blade Material", InputType.DROPDOWN)
    create_attribute_options(blade_material_attr, ["Steel", "Fiberglass"])
    
    # Air Compressors
    air_compressors = create_category("Air Compressors", tools_equipment)
    
    # Tank Capacity
    create_attribute(air_compressors, "Tank Capacity", InputType.NUMBER, "Liters")
    
    # Pressure
    create_attribute(air_compressors, "Pressure", InputType.NUMBER, "PSI")
    
    # Motor Power
    create_attribute(air_compressors, "Motor Power", InputType.NUMBER, "HP")
    
    # Multimeters
    multimeters = create_category("Multimeters", tools_equipment)
    
    # Display Type
    display_type_attr = create_attribute(multimeters, "Display Type", InputType.DROPDOWN)
    create_attribute_options(display_type_attr, ["Analog", "Digital"])
    
    # Auto Range
    auto_range_attr = create_attribute(multimeters, "Auto Range", InputType.BOOLEAN)
    create_attribute_options(auto_range_attr, ["Yes", "No"])
    
    # Measurement Functions
    create_attribute(multimeters, "Measurement Functions", InputType.TEXT)
    
    # Ladders
    ladders = create_category("Ladders", tools_equipment)
    
    # Type
    ladder_type_attr = create_attribute(ladders, "Type", InputType.DROPDOWN)
    create_attribute_options(ladder_type_attr, ["Step", "Extension", "Telescopic"])
    
    # Height
    create_attribute(ladders, "Height", InputType.NUMBER, "feet")
    
    # Material
    ladder_material_attr = create_attribute(ladders, "Material", InputType.DROPDOWN)
    create_attribute_options(ladder_material_attr, ["Aluminum", "Fiberglass"])
    
    # Angle Grinders
    angle_grinders = create_category("Angle Grinders", tools_equipment)
    
    # Disc Diameter
    create_attribute(angle_grinders, "Disc Diameter", InputType.NUMBER, "mm")
    
    # Power Input
    create_attribute(angle_grinders, "Power Input", InputType.NUMBER, "Watts")
    
    # Speed
    create_attribute(angle_grinders, "Speed", InputType.NUMBER, "RPM")
    
    # Tool Kits
    tool_kits = create_category("Tool Kits", tools_equipment)
    
    # Number of Tools
    create_attribute(tool_kits, "Number of Tools", InputType.NUMBER)
    
    # Case Included
    case_attr = create_attribute(tool_kits, "Case Included", InputType.BOOLEAN)
    create_attribute_options(case_attr, ["Yes", "No"])
    
    # Brand
    tool_brand_attr = create_attribute(tool_kits, "Brand", InputType.DROPDOWN)
    create_attribute_options(tool_brand_attr, ["Bosch", "Black+Decker", "Stanley"])
    
    # Chainsaws
    chainsaws = create_category("Chainsaws", tools_equipment)
    
    # Power Source
    power_source_attr = create_attribute(chainsaws, "Power Source", InputType.DROPDOWN)
    create_attribute_options(power_source_attr, ["Electric", "Petrol", "Battery"])
    
    # Bar Length
    create_attribute(chainsaws, "Bar Length", InputType.NUMBER, "inches")
    
    # Chain Speed
    create_attribute(chainsaws, "Chain Speed", InputType.NUMBER, "m/s")

def populate_sports_outdoor():
    """Populate Sports and Outdoor category and subcategories"""
    sports_outdoor = create_category("Sports and Outdoor")
    
    # Treadmills
    treadmills = create_category("Treadmills", sports_outdoor)
    
    # Motor Power
    create_attribute(treadmills, "Motor Power", InputType.NUMBER, "HP")
    
    # Max Speed
    create_attribute(treadmills, "Max Speed", InputType.NUMBER, "km/h")
    
    # Incline
    incline_attr = create_attribute(treadmills, "Incline", InputType.BOOLEAN)
    create_attribute_options(incline_attr, ["Yes", "No"])
    
    # Foldable
    foldable_attr = create_attribute(treadmills, "Foldable", InputType.BOOLEAN)
    create_attribute_options(foldable_attr, ["Yes", "No"])
    
    # Dumbbell Sets
    dumbbell_sets = create_category("Dumbbell Sets", sports_outdoor)
    
    # Total Weight
    create_attribute(dumbbell_sets, "Total Weight", InputType.NUMBER, "kg")
    
    # Adjustable
    adjustable_dumbbell_attr = create_attribute(dumbbell_sets, "Adjustable", InputType.BOOLEAN)
    create_attribute_options(adjustable_dumbbell_attr, ["Yes", "No"])
    
    # Material
    dumbbell_material_attr = create_attribute(dumbbell_sets, "Material", InputType.DROPDOWN)
    create_attribute_options(dumbbell_material_attr, ["Rubber", "Cast Iron", "Vinyl"])
    
    # Football Shoes
    football_shoes = create_category("Football Shoes", sports_outdoor)
    
    # Size
    create_attribute(football_shoes, "Size", InputType.NUMBER)
    
    # Stud Type
    stud_type_attr = create_attribute(football_shoes, "Stud Type", InputType.DROPDOWN)
    create_attribute_options(stud_type_attr, ["Firm Ground", "Soft Ground", "Turf"])
    
    # Material
    football_material_attr = create_attribute(football_shoes, "Material", InputType.DROPDOWN)
    create_attribute_options(football_material_attr, ["Synthetic", "Leather"])
    
    # Bicycles
    bicycles = create_category("Bicycles", sports_outdoor)
    
    # Type
    bicycle_type_attr = create_attribute(bicycles, "Type", InputType.DROPDOWN)
    create_attribute_options(bicycle_type_attr, ["Road", "Mountain", "Hybrid"])
    
    # Frame Size
    create_attribute(bicycles, "Frame Size", InputType.NUMBER, "inches")
    
    # Gear Count
    create_attribute(bicycles, "Gear Count", InputType.NUMBER)
    
    # Cricket Bats
    cricket_bats = create_category("Cricket Bats", sports_outdoor)
    
    # Size
    bat_size_attr = create_attribute(cricket_bats, "Size", InputType.DROPDOWN)
    create_attribute_options(bat_size_attr, ["4", "5", "6", "Full"])
    
    # Willow Type
    willow_attr = create_attribute(cricket_bats, "Willow Type", InputType.DROPDOWN)
    create_attribute_options(willow_attr, ["English", "Kashmir"])
    
    # Weight
    create_attribute(cricket_bats, "Weight", InputType.NUMBER, "grams")
    
    # Camping Tents
    camping_tents = create_category("Camping Tents", sports_outdoor)
    
    # Capacity
    create_attribute(camping_tents, "Capacity", InputType.NUMBER, "persons")
    
    # Waterproof
    tent_waterproof_attr = create_attribute(camping_tents, "Waterproof", InputType.BOOLEAN)
    create_attribute_options(tent_waterproof_attr, ["Yes", "No"])
    
    # Setup Type
    setup_attr = create_attribute(camping_tents, "Setup Type", InputType.DROPDOWN)
    create_attribute_options(setup_attr, ["Manual", "Pop-up"])
    
    # Yoga Mats
    yoga_mats = create_category("Yoga Mats", sports_outdoor)
    
    # Thickness
    create_attribute(yoga_mats, "Thickness", InputType.NUMBER, "mm")
    
    # Material
    mat_material_attr = create_attribute(yoga_mats, "Material", InputType.DROPDOWN)
    create_attribute_options(mat_material_attr, ["PVC", "TPE", "Rubber"])
    
    # Non-Slip
    non_slip_attr = create_attribute(yoga_mats, "Non-Slip", InputType.BOOLEAN)
    create_attribute_options(non_slip_attr, ["Yes", "No"])
    
    # Skates
    skates = create_category("Skates", sports_outdoor)
    
    # Type
    skate_type_attr = create_attribute(skates, "Type", InputType.DROPDOWN)
    create_attribute_options(skate_type_attr, ["Inline", "Quad"])
    
    # Size
    create_attribute(skates, "Size", InputType.NUMBER)
    
    # Adjustable Size
    adjustable_skate_attr = create_attribute(skates, "Adjustable Size", InputType.BOOLEAN)
    create_attribute_options(adjustable_skate_attr, ["Yes", "No"])
    
    # Badminton Rackets
    badminton_rackets = create_category("Badminton Rackets", sports_outdoor)
    
    # Weight
    racket_weight_attr = create_attribute(badminton_rackets, "Weight", InputType.DROPDOWN)
    create_attribute_options(racket_weight_attr, ["3U", "4U", "5U"])
    
    # Material
    racket_material_attr = create_attribute(badminton_rackets, "Material", InputType.DROPDOWN)
    create_attribute_options(racket_material_attr, ["Aluminum", "Graphite"])
    
    # Flexibility
    flexibility_attr = create_attribute(badminton_rackets, "Flexibility", InputType.DROPDOWN)
    create_attribute_options(flexibility_attr, ["Stiff", "Medium", "Flexible"])
    
    # Boxing Gloves
    boxing_gloves = create_category("Boxing Gloves", sports_outdoor)
    
    # Weight
    glove_weight_attr = create_attribute(boxing_gloves, "Weight", InputType.DROPDOWN)
    create_attribute_options(glove_weight_attr, ["10oz", "12oz", "14oz", "16oz"])
    
    # Material
    glove_material_attr = create_attribute(boxing_gloves, "Material", InputType.DROPDOWN)
    create_attribute_options(glove_material_attr, ["PU", "Leather"])
    
    # Strap Type
    strap_type_attr = create_attribute(boxing_gloves, "Strap Type", InputType.DROPDOWN)
    create_attribute_options(strap_type_attr, ["Velcro", "Lace-up"])

def populate_animals_pets():
    """Populate Animals and Pets category and subcategories"""
    animals_pets = create_category("Animals and Pets")
    
    # Dog Food
    dog_food = create_category("Dog Food", animals_pets)
    
    # Breed Size
    breed_size_attr = create_attribute(dog_food, "Breed Size", InputType.DROPDOWN)
    create_attribute_options(breed_size_attr, ["Small", "Medium", "Large"])
    
    # Flavor
    flavor_attr = create_attribute(dog_food, "Flavor", InputType.DROPDOWN)
    create_attribute_options(flavor_attr, ["Chicken", "Beef", "Lamb", "Fish"])
    
    # Weight
    create_attribute(dog_food, "Weight", InputType.NUMBER, "kg")
    
    # Age Group
    age_group_attr = create_attribute(dog_food, "Age Group", InputType.DROPDOWN)
    create_attribute_options(age_group_attr, ["Puppy", "Adult", "Senior"])
    
    # Cat Litter
    cat_litter = create_category("Cat Litter", animals_pets)
    
    # Type
    litter_type_attr = create_attribute(cat_litter, "Type", InputType.DROPDOWN)
    create_attribute_options(litter_type_attr, ["Clumping", "Non-Clumping"])
    
    # Scented
    scented_attr = create_attribute(cat_litter, "Scented", InputType.BOOLEAN)
    create_attribute_options(scented_attr, ["Yes", "No"])
    
    # Weight
    create_attribute(cat_litter, "Weight", InputType.NUMBER, "kg")
    
    # Bird Cages
    bird_cages = create_category("Bird Cages", animals_pets)
    
    # Size
    cage_size_attr = create_attribute(bird_cages, "Size", InputType.DROPDOWN)
    create_attribute_options(cage_size_attr, ["Small", "Medium", "Large"])
    
    # Material
    cage_material_attr = create_attribute(bird_cages, "Material", InputType.DROPDOWN)
    create_attribute_options(cage_material_attr, ["Iron", "Stainless Steel", "Plastic"])
    
    # Number of Doors
    create_attribute(bird_cages, "Number of Doors", InputType.NUMBER)
    
    # Fish Tanks
    fish_tanks = create_category("Fish Tanks", animals_pets)
    
    # Capacity
    create_attribute(fish_tanks, "Capacity", InputType.NUMBER, "Liters")
    
    # Glass Type
    glass_type_attr = create_attribute(fish_tanks, "Glass Type", InputType.DROPDOWN)
    create_attribute_options(glass_type_attr, ["Acrylic", "Glass"])
    
    # Filter Included
    filter_attr = create_attribute(fish_tanks, "Filter Included", InputType.BOOLEAN)
    create_attribute_options(filter_attr, ["Yes", "No"])
    
    # Pet Toys
    pet_toys = create_category("Pet Toys", animals_pets)
    
    # Type
    toy_type_attr = create_attribute(pet_toys, "Type", InputType.DROPDOWN)
    create_attribute_options(toy_type_attr, ["Chew", "Plush", "Interactive"])
    
    # Material
    toy_material_attr = create_attribute(pet_toys, "Material", InputType.DROPDOWN)
    create_attribute_options(toy_material_attr, ["Rubber", "Nylon", "Rope"])
    
    # Leashes
    leashes = create_category("Leashes", animals_pets)
    
    # Length
    create_attribute(leashes, "Length", InputType.NUMBER, "feet")
    
    # Material
    leash_material_attr = create_attribute(leashes, "Material", InputType.DROPDOWN)
    create_attribute_options(leash_material_attr, ["Nylon", "Leather", "Chain"])
    
    # Retractable
    retractable_attr = create_attribute(leashes, "Retractable", InputType.BOOLEAN)
    create_attribute_options(retractable_attr, ["Yes", "No"])
    
    # Dog Beds
    dog_beds = create_category("Dog Beds", animals_pets)
    
    # Size
    bed_size_attr = create_attribute(dog_beds, "Size", InputType.DROPDOWN)
    create_attribute_options(bed_size_attr, ["Small", "Medium", "Large"])
    
    # Washable Cover
    washable_attr = create_attribute(dog_beds, "Washable Cover", InputType.BOOLEAN)
    create_attribute_options(washable_attr, ["Yes", "No"])
    
    # Shape
    bed_shape_attr = create_attribute(dog_beds, "Shape", InputType.DROPDOWN)
    create_attribute_options(bed_shape_attr, ["Round", "Rectangular", "Oval"])
    
    # Aquarium Accessories
    aquarium_accessories = create_category("Aquarium Accessories", animals_pets)
    
    # Type
    aquarium_type_attr = create_attribute(aquarium_accessories, "Type", InputType.DROPDOWN)
    create_attribute_options(aquarium_type_attr, ["Filter", "Air Pump", "Decor"])
    
    # Voltage
    create_attribute(aquarium_accessories, "Voltage", InputType.NUMBER, "V")
    
    # Brand
    create_attribute(aquarium_accessories, "Brand", InputType.TEXT)
    
    # Pet Grooming Kits
    grooming_kits = create_category("Pet Grooming Kits", animals_pets)
    
    # Number of Tools
    create_attribute(grooming_kits, "Number of Tools", InputType.NUMBER)
    
    # Electric Clipper Included
    clipper_attr = create_attribute(grooming_kits, "Electric Clipper Included", InputType.BOOLEAN)
    create_attribute_options(clipper_attr, ["Yes", "No"])
    
    # Suitable For
    suitable_attr = create_attribute(grooming_kits, "Suitable For", InputType.DROPDOWN)
    create_attribute_options(suitable_attr, ["Dog", "Cat", "Both"])
    
    # Pet Carriers
    pet_carriers = create_category("Pet Carriers", animals_pets)
    
    # Size
    carrier_size_attr = create_attribute(pet_carriers, "Size", InputType.DROPDOWN)
    create_attribute_options(carrier_size_attr, ["S", "M", "L"])
    
    # Material
    carrier_material_attr = create_attribute(pet_carriers, "Material", InputType.DROPDOWN)
    create_attribute_options(carrier_material_attr, ["Plastic", "Fabric"])
    
    # Airline Approved
    airline_attr = create_attribute(pet_carriers, "Airline Approved", InputType.BOOLEAN)
    create_attribute_options(airline_attr, ["Yes", "No"])

def populate_machinery_tools():
    """Populate Machinery Tools category and subcategories"""
    machinery_tools = create_category("Machinery Tools")
    
    # Industrial Generators
    industrial_generators = create_category("Industrial Generators", machinery_tools)
    
    # Power Output
    create_attribute(industrial_generators, "Power Output", InputType.NUMBER, "kVA")
    
    # Fuel Type
    generator_fuel_attr = create_attribute(industrial_generators, "Fuel Type", InputType.DROPDOWN)
    create_attribute_options(generator_fuel_attr, ["Diesel", "Petrol", "Gas"])
    
    # Phase
    phase_attr = create_attribute(industrial_generators, "Phase", InputType.DROPDOWN)
    create_attribute_options(phase_attr, ["Single", "Three"])
    
    # CNC Machines
    cnc_machines = create_category("CNC Machines", machinery_tools)
    
    # Type
    cnc_type_attr = create_attribute(cnc_machines, "Type", InputType.DROPDOWN)
    create_attribute_options(cnc_type_attr, ["Milling", "Lathe", "Router"])
    
    # Axis Count
    create_attribute(cnc_machines, "Axis Count", InputType.NUMBER)
    
    # Power Supply
    create_attribute(cnc_machines, "Power Supply", InputType.NUMBER, "V")
    
    # Hydraulic Presses
    hydraulic_presses = create_category("Hydraulic Presses", machinery_tools)
    
    # Capacity
    create_attribute(hydraulic_presses, "Capacity", InputType.NUMBER, "Tons")
    
    # Bed Size
    create_attribute(hydraulic_presses, "Bed Size", InputType.TEXT)
    
    # Control Type
    control_type_attr = create_attribute(hydraulic_presses, "Control Type", InputType.DROPDOWN)
    create_attribute_options(control_type_attr, ["Manual", "Automatic"])
    
    # Lathe Machines
    lathe_machines = create_category("Lathe Machines", machinery_tools)
    
    # Swing Over Bed
    create_attribute(lathe_machines, "Swing Over Bed", InputType.NUMBER, "mm")
    
    # Distance Between Centers
    create_attribute(lathe_machines, "Distance Between Centers", InputType.NUMBER, "mm")
    
    # Motor Power
    create_attribute(lathe_machines, "Motor Power", InputType.NUMBER, "HP")
    
    # Forklifts
    forklifts = create_category("Forklifts", machinery_tools)
    
    # Load Capacity
    create_attribute(forklifts, "Load Capacity", InputType.NUMBER, "kg")
    
    # Fuel Type
    forklift_fuel_attr = create_attribute(forklifts, "Fuel Type", InputType.DROPDOWN)
    create_attribute_options(forklift_fuel_attr, ["Diesel", "Electric", "Gas"])
    
    # Lift Height
    create_attribute(forklifts, "Lift Height", InputType.NUMBER, "meters")
    
    # Air Handling Units
    air_handling_units = create_category("Air Handling Units", machinery_tools)
    
    # Air Flow
    create_attribute(air_handling_units, "Air Flow", InputType.NUMBER, "CFM")
    
    # Voltage
    create_attribute(air_handling_units, "Voltage", InputType.NUMBER, "V")
    
    # Control Panel Included
    control_panel_attr = create_attribute(air_handling_units, "Control Panel Included", InputType.BOOLEAN)
    create_attribute_options(control_panel_attr, ["Yes", "No"])
    
    # Water Pumps
    water_pumps = create_category("Water Pumps", machinery_tools)
    
    # Flow Rate
    create_attribute(water_pumps, "Flow Rate", InputType.NUMBER, "L/min")
    
    # Head Height
    create_attribute(water_pumps, "Head Height", InputType.NUMBER, "meters")
    
    # Power Source
    pump_power_attr = create_attribute(water_pumps, "Power Source", InputType.DROPDOWN)
    create_attribute_options(pump_power_attr, ["Electric", "Diesel"])
    
    # Industrial Vacuum Cleaners
    industrial_vacuums = create_category("Industrial Vacuum Cleaners", machinery_tools)
    
    # Capacity
    create_attribute(industrial_vacuums, "Capacity", InputType.NUMBER, "Liters")
    
    # Type
    vacuum_type_attr = create_attribute(industrial_vacuums, "Type", InputType.DROPDOWN)
    create_attribute_options(vacuum_type_attr, ["Wet & Dry", "Dry Only"])
    
    # Cord Length
    create_attribute(industrial_vacuums, "Cord Length", InputType.NUMBER, "meters")
    
    # Welding Generators
    welding_generators = create_category("Welding Generators", machinery_tools)
    
    # Output Current
    create_attribute(welding_generators, "Output Current", InputType.NUMBER, "Amps")
    
    # Engine Type
    engine_type_attr = create_attribute(welding_generators, "Engine Type", InputType.DROPDOWN)
    create_attribute_options(engine_type_attr, ["Petrol", "Diesel"])
    
    # Duty Cycle
    create_attribute(welding_generators, "Duty Cycle", InputType.TEXT)
    
    # Material Handling Cranes
    material_cranes = create_category("Material Handling Cranes", machinery_tools)
    
    # Type
    crane_type_attr = create_attribute(material_cranes, "Type", InputType.DROPDOWN)
    create_attribute_options(crane_type_attr, ["Gantry", "Overhead", "Jib"])
    
    # Load Capacity
    create_attribute(material_cranes, "Load Capacity", InputType.NUMBER, "Tons")
    
    # Span
    create_attribute(material_cranes, "Span", InputType.NUMBER, "meters")

def main():
    """Main function to populate all categories and attributes"""
    print("Starting to populate remaining categories and attributes...")
    
    # Populate Home Interiors
    print("Populating Home Interiors...")
    populate_home_interiors()
    
    # Populate Computer and Tech
    print("Populating Computer and Tech...")
    populate_computer_tech()
    
    # Populate Tools and Equipment
    print("Populating Tools and Equipment...")
    populate_tools_equipment()
    
    # Populate Sports and Outdoor
    print("Populating Sports and Outdoor...")
    populate_sports_outdoor()
    
    # Populate Animals and Pets
    print("Populating Animals and Pets...")
    populate_animals_pets()
    
    # Populate Machinery Tools
    print("Populating Machinery Tools...")
    populate_machinery_tools()
    
    print("All categories and attributes populated successfully!")

if __name__ == "__main__":
    main() 