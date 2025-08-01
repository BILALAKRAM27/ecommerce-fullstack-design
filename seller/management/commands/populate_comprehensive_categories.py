from django.core.management.base import BaseCommand
from seller.models import Category, CategoryAttribute, AttributeOption


class Command(BaseCommand):
    help = 'Populate database with comprehensive categories, subcategories, and attributes'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive categories and attributes...')

        # Define the complete category structure
        categories_data = {
            'Automobiles': {
                'description': 'Automotive vehicles and accessories',
                'subcategories': {
                    'Cars': 'Automotive vehicles for personal use',
                    'Motorcycles': 'Two-wheeled motor vehicles',
                    'Car Accessories': 'Accessories and parts for cars',
                    'Tyres & Rims': 'Tires and wheel rims',
                    'Auto Electronics': 'Electronic components for vehicles'
                },
                'attributes': {
                    'Fuel Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Petrol', 'Diesel', 'Hybrid', 'Electric', 'CNG']
                    },
                    'Transmission': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Manual', 'Automatic', 'CVT', 'Semi-Automatic', 'Tiptronic']
                    },
                    'Engine Capacity (cc)': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'unit': 'cc',
                        'options': ['800', '1000', '1300', '1500', '1800']
                    },
                    'Condition': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['New', 'Used', 'Certified', 'Refurbished', 'Damaged']
                    },
                    'Color': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Black', 'White', 'Silver', 'Blue', 'Red']
                    }
                }
            },
            'Clothes and Wear': {
                'description': 'Apparel and fashion items',
                'subcategories': {
                    "Men's Clothing": 'Clothing for men',
                    "Women's Clothing": 'Clothing for women',
                    "Kids' Wear": 'Clothing for children',
                    'Shoes': 'Footwear for all ages',
                    'Accessories': 'Fashion accessories and jewelry'
                },
                'attributes': {
                    'Size': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['S', 'M', 'L', 'XL', 'XXL']
                    },
                    'Material': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Cotton', 'Polyester', 'Denim', 'Silk', 'Wool']
                    },
                    'Color': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Black', 'White', 'Red', 'Blue', 'Green']
                    },
                    'Pattern': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Solid', 'Striped', 'Floral', 'Checked', 'Printed']
                    },
                    'Occasion': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Casual', 'Formal', 'Sportswear', 'Party', 'Daily']
                    }
                }
            },
            'Home Interiors': {
                'description': 'Home decoration and furniture',
                'subcategories': {
                    'Furniture': 'Home and office furniture',
                    'Lighting': 'Lighting fixtures and lamps',
                    'Wall Decor': 'Wall decorations and art',
                    'Bedding': 'Bed sheets, pillows, and bedding',
                    'Kitchen Essentials': 'Kitchen tools and accessories'
                },
                'attributes': {
                    'Material': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Wood', 'Metal', 'Plastic', 'Glass', 'Fabric']
                    },
                    'Style': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Modern', 'Traditional', 'Vintage', 'Minimalist', 'Rustic']
                    },
                    'Color': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Brown', 'White', 'Black', 'Grey', 'Beige']
                    },
                    'Dimensions (cm)': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'unit': 'cm',
                        'options': ['100x50x75', '120x60x80', '150x70x90', '180x80x100', '200x90x110']
                    },
                    'Weight Capacity': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'unit': 'kg',
                        'options': ['50kg', '75kg', '100kg', '150kg', '200kg']
                    }
                }
            },
            'Computer and Tech': {
                'description': 'Computers, electronics, and technology',
                'subcategories': {
                    'Laptops': 'Portable computers',
                    'Desktop Computers': 'Desktop computers and towers',
                    'Computer Accessories': 'Computer peripherals and accessories',
                    'Mobile Phones': 'Smartphones and mobile devices',
                    'Smart Devices': 'Smart home and IoT devices'
                },
                'attributes': {
                    'RAM': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'unit': 'GB',
                        'options': ['4GB', '8GB', '16GB', '32GB', '64GB']
                    },
                    'Storage Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['HDD', 'SSD', 'NVMe', 'Hybrid', 'eMMC']
                    },
                    'Processor': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Intel i5', 'Intel i7', 'AMD Ryzen 5', 'M1', 'M2']
                    },
                    'Operating System': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Windows', 'macOS', 'Linux', 'ChromeOS', 'Android']
                    },
                    'Screen Size (inches)': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'unit': 'inches',
                        'options': ['13"', '14"', '15.6"', '17"', '24"']
                    }
                }
            },
            'Tools and Equipment': {
                'description': 'Tools and equipment for various purposes',
                'subcategories': {
                    'Power Tools': 'Electric and battery-powered tools',
                    'Hand Tools': 'Manual tools and equipment',
                    'Garden Tools': 'Gardening and landscaping tools',
                    'Industrial Equipment': 'Industrial machinery and equipment',
                    'Measuring Tools': 'Measurement and precision tools'
                },
                'attributes': {
                    'Power Source': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Electric', 'Battery', 'Manual', 'Petrol', 'Cordless']
                    },
                    'Brand': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Bosch', 'DeWalt', 'Black+Decker', 'Makita', 'Stanley']
                    },
                    'Tool Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Drill', 'Grinder', 'Saw', 'Wrench', 'Screwdriver']
                    },
                    'Voltage (V)': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'unit': 'V',
                        'options': ['12V', '18V', '20V', '24V', '36V']
                    },
                    'Usage': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['DIY', 'Industrial', 'Professional', 'Home Use', 'Heavy Duty']
                    }
                }
            },
            'Sports and Outdoor': {
                'description': 'Sports equipment and outdoor gear',
                'subcategories': {
                    'Sportswear': 'Sports clothing and athletic wear',
                    'Fitness Equipment': 'Exercise and fitness equipment',
                    'Camping Gear': 'Camping and outdoor equipment',
                    'Bicycles': 'Bicycles and cycling accessories',
                    'Balls & Rackets': 'Sports balls and racket sports equipment'
                },
                'attributes': {
                    'Size': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['XS', 'S', 'M', 'L', 'XL']
                    },
                    'Activity Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Running', 'Gym', 'Cycling', 'Hiking', 'Swimming']
                    },
                    'Material': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Nylon', 'Spandex', 'Polyester', 'Mesh', 'Rubber']
                    },
                    'Weight (kg)': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'unit': 'kg',
                        'options': ['1kg', '2kg', '5kg', '10kg', '15kg']
                    },
                    'Waterproof': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Yes', 'No']
                    }
                }
            },
            'Animals and Pets': {
                'description': 'Pet supplies and animal care products',
                'subcategories': {
                    'Pet Food': 'Food and nutrition for pets',
                    'Pet Accessories': 'Pet accessories and equipment',
                    'Grooming Products': 'Pet grooming and hygiene products',
                    'Pet Toys': 'Toys and entertainment for pets',
                    'Veterinary Supplies': 'Medical supplies for pets'
                },
                'attributes': {
                    'Pet Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit']
                    },
                    'Food Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Dry', 'Wet', 'Raw', 'Grain-Free', 'Organic']
                    },
                    'Size': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Small', 'Medium', 'Large', 'X-Large', 'Puppy/Kitten']
                    },
                    'Age Group': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Puppy', 'Adult', 'Senior', 'Kitten', 'All Ages']
                    },
                    'Flavor': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['Chicken', 'Beef', 'Fish', 'Lamb', 'Mixed']
                    }
                }
            },
            'Machinery Tools': {
                'description': 'Heavy machinery and industrial tools',
                'subcategories': {
                    'Construction Machines': 'Construction and building machinery',
                    'Agricultural Tools': 'Farming and agricultural equipment',
                    'Heavy Equipment': 'Heavy industrial machinery',
                    'Industrial Machinery': 'Industrial manufacturing equipment',
                    'Generators': 'Power generators and electrical equipment'
                },
                'attributes': {
                    'Power Source': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Diesel', 'Petrol', 'Electric', 'Hybrid', 'Manual']
                    },
                    'Capacity': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'unit': 'tons',
                        'options': ['5 tons', '10 tons', '15 tons', '20 tons', '30 tons']
                    },
                    'Usage Type': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['Construction', 'Farming', 'Industrial', 'DIY', 'Commercial']
                    },
                    'Condition': {
                        'input_type': 'dropdown',
                        'is_required': True,
                        'options': ['New', 'Used', 'Reconditioned', 'Refurbished', 'Damaged']
                    },
                    'Operating Hours': {
                        'input_type': 'dropdown',
                        'is_required': False,
                        'options': ['<1000', '1000–5000', '5000–10000', '>10000', 'Unknown']
                    }
                }
            }
        }

        created_categories = []
        created_subcategories = []
        created_attributes = []
        created_options = []

        # Create categories and their subcategories
        for category_name, category_data in categories_data.items():
            # Create or get main category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': category_data['description']}
            )
            if created:
                created_categories.append(category_name)
                self.stdout.write(f'Created category: {category_name}')

            # Create subcategories
            for subcategory_name, subcategory_description in category_data['subcategories'].items():
                subcategory, created = Category.objects.get_or_create(
                    name=subcategory_name,
                    parent=category,
                    defaults={'description': subcategory_description}
                )
                if created:
                    created_subcategories.append(subcategory_name)
                    self.stdout.write(f'Created subcategory: {subcategory_name}')

                # Create attributes for subcategory
                for attr_name, attr_data in category_data['attributes'].items():
                    attribute, created = CategoryAttribute.objects.get_or_create(
                        name=attr_name,
                        category=subcategory,
                        defaults={
                            'input_type': attr_data['input_type'],
                            'is_required': attr_data['is_required'],
                            'unit': attr_data.get('unit', '')
                        }
                    )
                    if created:
                        created_attributes.append(f'{subcategory_name} - {attr_name}')
                        self.stdout.write(f'Created attribute: {attr_name} for {subcategory_name}')

                    # Create attribute options
                    for option_value in attr_data['options']:
                        option, created = AttributeOption.objects.get_or_create(
                            attribute=attribute,
                            value=option_value
                        )
                        if created:
                            created_options.append(f'{attr_name} - {option_value}')
                            self.stdout.write(f'Created option: {option_value} for {attr_name}')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Population Summary ==='))
        self.stdout.write(f'Categories created: {len(created_categories)}')
        self.stdout.write(f'Subcategories created: {len(created_subcategories)}')
        self.stdout.write(f'Attributes created: {len(created_attributes)}')
        self.stdout.write(f'Attribute options created: {len(created_options)}')
        
        if created_categories:
            self.stdout.write(f'\nNew categories: {", ".join(created_categories)}')
        if created_subcategories:
            self.stdout.write(f'New subcategories: {", ".join(created_subcategories[:10])}{"..." if len(created_subcategories) > 10 else ""}')
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated categories and attributes!')) 