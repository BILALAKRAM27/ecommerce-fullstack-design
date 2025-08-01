from django.core.management.base import BaseCommand
from seller.models import Brand


class Command(BaseCommand):
    help = 'Populate database with comprehensive brand list'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive brand list...')

        # Define all brands
        brands_list = [
            # Electronics & Tech
            'Samsung',
            'Sony', 
            'LG',
            'Apple',
            'Dell',
            'HP',
            
            # Fashion & Clothing
            'Levi',
            'Zara',
            'Nike',
            'Adidas',
            'H&M',
            'Alkaram',
            
            # Automotive
            'Toyota',
            'Tesla',
            'Honda',
            'BMW',
            'Mercedes',
            
            # Home & Furniture
            'IKEA',
            'Ashley HomeStore',
            'West Elm',
            
            # Tools & Equipment
            'DeWalt',
            'Makita',
            'Bosch',
            
            # Sports & Outdoor
            'Decathlon',
            'Columbia',
            'The North Face',
            
            # Pet Supplies
            'Pedigree',
            'Whiskas',
            'Trixie',
            
            # Heavy Machinery
            'Caterpillar (CAT)',
            'John Deere',
            'Komatsu'
        ]

        created_brands = []
        existing_brands = []

        # Create brands
        for brand_name in brands_list:
            brand, created = Brand.objects.get_or_create(
                name=brand_name
            )
            
            if created:
                created_brands.append(brand_name)
                self.stdout.write(f'Created brand: {brand_name}')
            else:
                existing_brands.append(brand_name)
                self.stdout.write(f'Brand already exists: {brand_name}')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Brand Population Summary ==='))
        self.stdout.write(f'Total brands processed: {len(brands_list)}')
        self.stdout.write(f'New brands created: {len(created_brands)}')
        self.stdout.write(f'Existing brands found: {len(existing_brands)}')
        
        if created_brands:
            self.stdout.write(f'\nNew brands: {", ".join(created_brands)}')
        if existing_brands:
            self.stdout.write(f'Existing brands: {", ".join(existing_brands)}')
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated brands!')) 