from django.core.management.base import BaseCommand
from seller.models import Category, CategoryAttribute, AttributeOption


class Command(BaseCommand):
    help = 'Populate sample attribute options for testing'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample attribute options...')
        
        # Get or create categories
        clothing_category = Category.objects.filter(name='Clothing').first()
        electronics_category = Category.objects.filter(name='Electronics').first()
        
        if not clothing_category:
            self.stdout.write('Clothing category not found. Please run populate_categories first.')
            return
            
        if not electronics_category:
            self.stdout.write('Electronics category not found. Please run populate_categories first.')
            return
        
        # Get or create attributes
        size_attr = CategoryAttribute.objects.filter(name='Size', category=clothing_category).first()
        color_attr = CategoryAttribute.objects.filter(name='Color', category=clothing_category).first()
        material_attr = CategoryAttribute.objects.filter(name='Material', category=clothing_category).first()
        
        brand_attr = CategoryAttribute.objects.filter(name='Brand', category=electronics_category).first()
        model_attr = CategoryAttribute.objects.filter(name='Model', category=electronics_category).first()
        warranty_attr = CategoryAttribute.objects.filter(name='Warranty', category=electronics_category).first()
        
        # Populate clothing attribute options
        if size_attr:
            size_options = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
            for size in size_options:
                AttributeOption.objects.get_or_create(
                    attribute=size_attr,
                    value=size
                )
            self.stdout.write(f'Created {len(size_options)} size options')
        
        if color_attr:
            color_options = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Gray']
            for color in color_options:
                AttributeOption.objects.get_or_create(
                    attribute=color_attr,
                    value=color
                )
            self.stdout.write(f'Created {len(color_options)} color options')
        
        if material_attr:
            material_options = ['Cotton', 'Polyester', 'Wool', 'Silk', 'Linen', 'Denim', 'Leather', 'Synthetic', 'Bamboo', 'Hemp']
            for material in material_options:
                AttributeOption.objects.get_or_create(
                    attribute=material_attr,
                    value=material
                )
            self.stdout.write(f'Created {len(material_options)} material options')
        
        # Populate electronics attribute options
        if brand_attr:
            brand_options = ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Microsoft', 'Google', 'Xiaomi']
            for brand in brand_options:
                AttributeOption.objects.get_or_create(
                    attribute=brand_attr,
                    value=brand
                )
            self.stdout.write(f'Created {len(brand_options)} brand options')
        
        if model_attr:
            model_options = ['iPhone 15', 'Galaxy S24', 'MacBook Pro', 'ThinkPad X1', 'Surface Pro', 'iPad Pro', 'AirPods Pro', 'Galaxy Tab', 'MacBook Air', 'Dell XPS']
            for model in model_options:
                AttributeOption.objects.get_or_create(
                    attribute=model_attr,
                    value=model
                )
            self.stdout.write(f'Created {len(model_options)} model options')
        
        if warranty_attr:
            warranty_options = ['1 Year', '2 Years', '3 Years', '5 Years', 'Lifetime', 'No Warranty', 'Extended Warranty']
            for warranty in warranty_options:
                AttributeOption.objects.get_or_create(
                    attribute=warranty_attr,
                    value=warranty
                )
            self.stdout.write(f'Created {len(warranty_options)} warranty options')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated attribute options!')) 