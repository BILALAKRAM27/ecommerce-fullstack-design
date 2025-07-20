from django.core.management.base import BaseCommand
from seller.models import Category, CategoryAttribute, AttributeOption


class Command(BaseCommand):
    help = 'Populate database with sample categories and attributes'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and attributes...')

        # Create Electronics category
        electronics = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )

        # Create Mobile subcategory
        mobile = Category.objects.create(
            name='Mobile Phones',
            parent=electronics,
            description='Smartphones and mobile devices'
        )

        # Create Laptop subcategory
        laptop = Category.objects.create(
            name='Laptops',
            parent=electronics,
            description='Portable computers'
        )

        # Create Mobile attributes
        ram_attr = CategoryAttribute.objects.create(
            category=mobile,
            name='RAM',
            input_type='dropdown',
            is_required=True,
            unit='GB'
        )

        storage_attr = CategoryAttribute.objects.create(
            category=mobile,
            name='Storage',
            input_type='dropdown',
            is_required=True,
            unit='GB'
        )

        color_attr = CategoryAttribute.objects.create(
            category=mobile,
            name='Color',
            input_type='dropdown',
            is_required=False
        )

        battery_attr = CategoryAttribute.objects.create(
            category=mobile,
            name='Battery Capacity',
            input_type='number',
            is_required=False,
            unit='mAh'
        )

        # Create RAM options
        AttributeOption.objects.create(attribute=ram_attr, value='4 GB')
        AttributeOption.objects.create(attribute=ram_attr, value='6 GB')
        AttributeOption.objects.create(attribute=ram_attr, value='8 GB')
        AttributeOption.objects.create(attribute=ram_attr, value='12 GB')
        AttributeOption.objects.create(attribute=ram_attr, value='16 GB')

        # Create Storage options
        AttributeOption.objects.create(attribute=storage_attr, value='64 GB')
        AttributeOption.objects.create(attribute=storage_attr, value='128 GB')
        AttributeOption.objects.create(attribute=storage_attr, value='256 GB')
        AttributeOption.objects.create(attribute=storage_attr, value='512 GB')
        AttributeOption.objects.create(attribute=storage_attr, value='1 TB')

        # Create Color options
        AttributeOption.objects.create(attribute=color_attr, value='Black')
        AttributeOption.objects.create(attribute=color_attr, value='White')
        AttributeOption.objects.create(attribute=color_attr, value='Blue')
        AttributeOption.objects.create(attribute=color_attr, value='Red')
        AttributeOption.objects.create(attribute=color_attr, value='Green')

        # Create Laptop attributes
        laptop_ram_attr = CategoryAttribute.objects.create(
            category=laptop,
            name='RAM',
            input_type='dropdown',
            is_required=True,
            unit='GB'
        )

        laptop_storage_attr = CategoryAttribute.objects.create(
            category=laptop,
            name='Storage',
            input_type='dropdown',
            is_required=True,
            unit='GB'
        )

        laptop_processor_attr = CategoryAttribute.objects.create(
            category=laptop,
            name='Processor',
            input_type='text',
            is_required=True
        )

        laptop_screen_attr = CategoryAttribute.objects.create(
            category=laptop,
            name='Screen Size',
            input_type='number',
            is_required=False,
            unit='inches'
        )

        # Create Laptop RAM options
        AttributeOption.objects.create(attribute=laptop_ram_attr, value='8 GB')
        AttributeOption.objects.create(attribute=laptop_ram_attr, value='16 GB')
        AttributeOption.objects.create(attribute=laptop_ram_attr, value='32 GB')
        AttributeOption.objects.create(attribute=laptop_ram_attr, value='64 GB')

        # Create Laptop Storage options
        AttributeOption.objects.create(attribute=laptop_storage_attr, value='256 GB')
        AttributeOption.objects.create(attribute=laptop_storage_attr, value='512 GB')
        AttributeOption.objects.create(attribute=laptop_storage_attr, value='1 TB')
        AttributeOption.objects.create(attribute=laptop_storage_attr, value='2 TB')

        # Create Clothing category
        clothing = Category.objects.create(
            name='Clothing',
            description='Apparel and fashion items'
        )

        # Create Men's Clothing subcategory
        mens_clothing = Category.objects.create(
            name="Men's Clothing",
            parent=clothing,
            description='Clothing for men'
        )

        # Create Women's Clothing subcategory
        womens_clothing = Category.objects.create(
            name="Women's Clothing",
            parent=clothing,
            description='Clothing for women'
        )

        # Create Clothing attributes
        size_attr = CategoryAttribute.objects.create(
            category=mens_clothing,
            name='Size',
            input_type='dropdown',
            is_required=True
        )

        material_attr = CategoryAttribute.objects.create(
            category=mens_clothing,
            name='Material',
            input_type='text',
            is_required=False
        )

        # Create Size options
        AttributeOption.objects.create(attribute=size_attr, value='XS')
        AttributeOption.objects.create(attribute=size_attr, value='S')
        AttributeOption.objects.create(attribute=size_attr, value='M')
        AttributeOption.objects.create(attribute=size_attr, value='L')
        AttributeOption.objects.create(attribute=size_attr, value='XL')
        AttributeOption.objects.create(attribute=size_attr, value='XXL')

        # Copy size attribute to women's clothing
        womens_size_attr = CategoryAttribute.objects.create(
            category=womens_clothing,
            name='Size',
            input_type='dropdown',
            is_required=True
        )

        # Create Women's Size options
        AttributeOption.objects.create(attribute=womens_size_attr, value='XS')
        AttributeOption.objects.create(attribute=womens_size_attr, value='S')
        AttributeOption.objects.create(attribute=womens_size_attr, value='M')
        AttributeOption.objects.create(attribute=womens_size_attr, value='L')
        AttributeOption.objects.create(attribute=womens_size_attr, value='XL')
        AttributeOption.objects.create(attribute=womens_size_attr, value='XXL')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample categories and attributes!')
        )
        self.stdout.write('Created categories: Electronics, Clothing')
        self.stdout.write('Created subcategories: Mobile Phones, Laptops, Men\'s Clothing, Women\'s Clothing')
        self.stdout.write('Created attributes: RAM, Storage, Color, Battery, Processor, Screen Size, Size, Material') 