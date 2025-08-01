from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Populate database with comprehensive categories, subcategories, attributes, and brands'

    def handle(self, *args, **options):
        self.stdout.write('Starting comprehensive data population...')
        
        # Populate categories and attributes
        self.stdout.write('\n=== Populating Categories and Attributes ===')
        call_command('populate_categories', verbosity=1)
        
        # Populate brands
        self.stdout.write('\n=== Populating Brands ===')
        call_command('populate_brands', verbosity=1)
        
        self.stdout.write(self.style.SUCCESS('\n=== All Data Population Complete ==='))
        self.stdout.write('✅ Categories, subcategories, and attributes populated')
        self.stdout.write('✅ Brands populated')
        self.stdout.write('\nYour database is now ready with comprehensive product data!') 