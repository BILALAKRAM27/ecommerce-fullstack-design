from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from seller.models import Seller, Category, Product
from buyer.models import Buyer
import random

class Command(BaseCommand):
    help = 'Populate sample stores and products for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample stores and products...')
        
        # Create categories if they don't exist
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
            {'name': 'Books', 'description': 'Books and media'},
            {'name': 'Health & Beauty', 'description': 'Health and beauty products'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            # Check if category exists, if multiple exist, use the first one
            try:
                category = Category.objects.filter(name=cat_data['name']).first()
                if not category:
                    category = Category.objects.create(
                        name=cat_data['name'],
                        description=cat_data['description']
                    )
                    self.stdout.write(f'Created category: {category.name}')
                else:
                    self.stdout.write(f'Using existing category: {category.name}')
            except Exception as e:
                self.stdout.write(f'Error with category {cat_data["name"]}: {e}')
                continue
                
            categories[cat_data['name']] = category
        
        # Create sample sellers
        sellers_data = [
            {
                'name': 'John Tech',
                'email': 'john@techhaven.com',
                'shop_name': 'Tech Haven',
                'shop_description': 'Premium electronics store with cutting-edge gadgets and devices.',
                'category': 'Electronics'
            },
            {
                'name': 'Sarah Fashion',
                'email': 'sarah@fashionforward.com',
                'shop_name': 'Fashion Forward',
                'shop_description': 'Trendy fashion and apparel for men and women.',
                'category': 'Clothing'
            },
            {
                'name': 'Mike Home',
                'email': 'mike@homecomfort.com',
                'shop_name': 'Home Comfort',
                'shop_description': 'Everything for your home and garden needs.',
                'category': 'Home & Garden'
            },
            {
                'name': 'Lisa Sports',
                'email': 'lisa@sportsworld.com',
                'shop_name': 'Sports World',
                'shop_description': 'Quality sports equipment and fitness gear.',
                'category': 'Sports'
            },
            {
                'name': 'David Books',
                'email': 'david@bookstore.com',
                'shop_name': 'Book Corner',
                'shop_description': 'Wide selection of books and educational materials.',
                'category': 'Books'
            },
        ]
        
        for seller_data in sellers_data:
            # Create user for seller
            user, created = User.objects.get_or_create(
                username=seller_data['email'],
                defaults={
                    'email': seller_data['email'],
                    'first_name': seller_data['name'].split()[0],
                    'last_name': seller_data['name'].split()[1] if len(seller_data['name'].split()) > 1 else '',
                }
            )
            
            # Create seller
            seller, created = Seller.objects.get_or_create(
                email=seller_data['email'],
                defaults={
                    'user': user,
                    'name': seller_data['name'],
                    'shop_name': seller_data['shop_name'],
                    'shop_description': seller_data['shop_description'],
                    'rating': round(random.uniform(3.5, 5.0), 1),
                }
            )
            
            if created:
                self.stdout.write(f'Created seller: {seller.shop_name}')
            
            # Create sample products for each seller
            category = categories[seller_data['category']]
            products_data = [
                {
                    'name': f'{seller_data["shop_name"]} Product 1',
                    'description': f'High-quality product from {seller_data["shop_name"]}',
                    'base_price': round(random.uniform(10, 500), 2),
                    'stock': random.randint(10, 100),
                },
                {
                    'name': f'{seller_data["shop_name"]} Product 2',
                    'description': f'Premium product from {seller_data["shop_name"]}',
                    'base_price': round(random.uniform(20, 800), 2),
                    'stock': random.randint(5, 50),
                },
                {
                    'name': f'{seller_data["shop_name"]} Product 3',
                    'description': f'Best-selling product from {seller_data["shop_name"]}',
                    'base_price': round(random.uniform(15, 300), 2),
                    'stock': random.randint(15, 75),
                },
            ]
            
            for product_data in products_data:
                product, created = Product.objects.get_or_create(
                    seller=seller,
                    name=product_data['name'],
                    defaults={
                        'category': category,
                        'description': product_data['description'],
                        'base_price': product_data['base_price'],
                        'stock': product_data['stock'],
                        'condition': 'new',
                        'rating_avg': round(random.uniform(3.0, 5.0), 1),
                        'order_count': random.randint(0, 50),
                    }
                )
                
                if created:
                    self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample stores and products!')
        ) 