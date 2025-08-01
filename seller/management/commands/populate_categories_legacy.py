from django.core.management.base import BaseCommand
from seller.models import Category, CategoryAttribute, AttributeOption


class Command(BaseCommand):
    help = 'Populate database with sample categories and attributes (legacy)'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and attributes...')

        # Create Electronics category (legacy)
        electronics, created = Category.objects.get_or_create(
            name='Electronics (Legacy)',
            defaults={'description': 'Electronic devices and gadgets (legacy)'}
        )
        if created:
            self.stdout.write('Created category: Electronics')

        # Create Mobile subcategory
        mobile, created = Category.objects.get_or_create(
            name='Mobile Phones',
            parent=electronics,
            defaults={'description': 'Smartphones and mobile devices'}
        )
        if created:
            self.stdout.write('Created subcategory: Mobile Phones')

        # Create Laptop subcategory
        laptop, created = Category.objects.get_or_create(
            name='Laptops',
            parent=electronics,
            defaults={'description': 'Portable computers'}
        )
        if created:
            self.stdout.write('Created subcategory: Laptops')

        # Create Mobile attributes
        ram_attr, created = CategoryAttribute.objects.get_or_create(
            category=mobile,
            name='RAM',
            defaults={
                'input_type': 'dropdown',
                'is_required': True,
                'unit': 'GB'
            }
        )
        if created:
            self.stdout.write('Created attribute: RAM for Mobile Phones')

        storage_attr, created = CategoryAttribute.objects.get_or_create(
            category=mobile,
            name='Storage',
            defaults={
                'input_type': 'dropdown',
                'is_required': True,
                'unit': 'GB'
            }
        )
        if created:
            self.stdout.write('Created attribute: Storage for Mobile Phones')

        color_attr, created = CategoryAttribute.objects.get_or_create(
            category=mobile,
            name='Color',
            defaults={
                'input_type': 'dropdown',
                'is_required': False
            }
        )
        if created:
            self.stdout.write('Created attribute: Color for Mobile Phones')

        battery_attr, created = CategoryAttribute.objects.get_or_create(
            category=mobile,
            name='Battery Capacity',
            defaults={
                'input_type': 'number',
                'is_required': False,
                'unit': 'mAh'
            }
        )
        if created:
            self.stdout.write('Created attribute: Battery Capacity for Mobile Phones')

        # Create RAM options
        ram_options = ['4 GB', '6 GB', '8 GB', '12 GB', '16 GB']
        for option in ram_options:
            AttributeOption.objects.get_or_create(attribute=ram_attr, value=option)

        # Create Storage options
        storage_options = ['64 GB', '128 GB', '256 GB', '512 GB', '1 TB']
        for option in storage_options:
            AttributeOption.objects.get_or_create(attribute=storage_attr, value=option)

        # Create Color options
        color_options = ['Black', 'White', 'Blue', 'Red', 'Green']
        for option in color_options:
            AttributeOption.objects.get_or_create(attribute=color_attr, value=option)

        # Create Laptop attributes
        laptop_ram_attr, created = CategoryAttribute.objects.get_or_create(
            category=laptop,
            name='RAM',
            defaults={
                'input_type': 'dropdown',
                'is_required': True,
                'unit': 'GB'
            }
        )
        if created:
            self.stdout.write('Created attribute: RAM for Laptops')

        laptop_storage_attr, created = CategoryAttribute.objects.get_or_create(
            category=laptop,
            name='Storage',
            defaults={
                'input_type': 'dropdown',
                'is_required': True,
                'unit': 'GB'
            }
        )
        if created:
            self.stdout.write('Created attribute: Storage for Laptops')

        laptop_processor_attr, created = CategoryAttribute.objects.get_or_create(
            category=laptop,
            name='Processor',
            defaults={
                'input_type': 'text',
                'is_required': True
            }
        )
        if created:
            self.stdout.write('Created attribute: Processor for Laptops')

        laptop_screen_attr, created = CategoryAttribute.objects.get_or_create(
            category=laptop,
            name='Screen Size',
            defaults={
                'input_type': 'number',
                'is_required': False,
                'unit': 'inches'
            }
        )
        if created:
            self.stdout.write('Created attribute: Screen Size for Laptops')

        # Create Laptop RAM options
        laptop_ram_options = ['8 GB', '16 GB', '32 GB', '64 GB']
        for option in laptop_ram_options:
            AttributeOption.objects.get_or_create(attribute=laptop_ram_attr, value=option)

        # Create Laptop Storage options
        laptop_storage_options = ['256 GB', '512 GB', '1 TB', '2 TB']
        for option in laptop_storage_options:
            AttributeOption.objects.get_or_create(attribute=laptop_storage_attr, value=option)

        # Create Clothing category (legacy)
        clothing, created = Category.objects.get_or_create(
            name='Clothing (Legacy)',
            defaults={'description': 'Apparel and fashion items (legacy)'}
        )
        if created:
            self.stdout.write('Created category: Clothing')

        # Create Men's Clothing subcategory
        mens_clothing, created = Category.objects.get_or_create(
            name="Men's Clothing",
            parent=clothing,
            defaults={'description': 'Clothing for men'}
        )
        if created:
            self.stdout.write('Created subcategory: Men\'s Clothing')

        # Create Women's Clothing subcategory
        womens_clothing, created = Category.objects.get_or_create(
            name="Women's Clothing",
            parent=clothing,
            defaults={'description': 'Clothing for women'}
        )
        if created:
            self.stdout.write('Created subcategory: Women\'s Clothing')

        # Create Clothing attributes
        size_attr, created = CategoryAttribute.objects.get_or_create(
            category=mens_clothing,
            name='Size',
            defaults={
                'input_type': 'dropdown',
                'is_required': True
            }
        )
        if created:
            self.stdout.write('Created attribute: Size for Men\'s Clothing')

        material_attr, created = CategoryAttribute.objects.get_or_create(
            category=mens_clothing,
            name='Material',
            defaults={
                'input_type': 'text',
                'is_required': False
            }
        )
        if created:
            self.stdout.write('Created attribute: Material for Men\'s Clothing')

        # Create Size options
        size_options = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        for option in size_options:
            AttributeOption.objects.get_or_create(attribute=size_attr, value=option)

        # Copy size attribute to women's clothing
        womens_size_attr, created = CategoryAttribute.objects.get_or_create(
            category=womens_clothing,
            name='Size',
            defaults={
                'input_type': 'dropdown',
                'is_required': True
            }
        )
        if created:
            self.stdout.write('Created attribute: Size for Women\'s Clothing')

        # Create Women's Size options
        for option in size_options:
            AttributeOption.objects.get_or_create(attribute=womens_size_attr, value=option)

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample categories and attributes!')
        )
        self.stdout.write('Created categories: Electronics (Legacy), Clothing (Legacy)')
        self.stdout.write('Created subcategories: Mobile Phones, Laptops, Men\'s Clothing, Women\'s Clothing')
        self.stdout.write('Created attributes: RAM, Storage, Color, Battery, Processor, Screen Size, Size, Material') 