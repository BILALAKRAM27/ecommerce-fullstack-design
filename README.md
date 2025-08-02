# MarketVibe - Multi-Vendor E-commerce Platform

A comprehensive multi-vendor e-commerce platform built with Django 5.2.4, featuring advanced seller/buyer management, Stripe Connect payment processing, dynamic product catalog, gift box campaigns, and robust order management system.

## 🚀 Features

### 🔐 Authentication & User Management
- **Dual User Types**: Separate registration and management for Buyers and Sellers
- **Secure Login**: Email-based authentication with password validation
- **Profile Management**: Complete profile management with image upload support (BLOB storage)
- **Account Deletion**: Secure account removal with complete data cleanup
- **Session Management**: Secure login/logout functionality with proper session handling

### 🛍️ Buyer Features
- **Buyer Registration**: Complete buyer account creation with profile setup
- **Profile Management**: Update buyer information, profile pictures, and contact details
- **Shopping Cart**: Advanced cart functionality with quantity management and AJAX updates
- **Wishlist Management**: Add/remove products to personal wishlist
- **Address Management**: Store and manage shipping addresses
- **Order History**: Complete order tracking and history
- **Product Reviews**: Rate and review purchased products with like/dislike system
- **Gift Box Orders**: Special gift box campaign ordering system
- **Order Tracking**: Real-time order status tracking with delivery estimates

### 🏪 Seller Features
- **Seller Registration**: Complete seller onboarding with shop details
- **Shop Management**: Manage shop name, description, and branding
- **Profile Management**: Update seller information and shop details
- **Image Upload**: Profile and product image storage as BLOB in database
- **Stripe Connect Integration**: Secure payment processing setup
- **Product Management**: Comprehensive product CRUD operations with dynamic forms
- **Inventory Management**: Stock tracking and management with low stock alerts
- **Order Management**: Process and track customer orders with status updates
- **Revenue Tracking**: Monitor sales, revenue, and payouts
- **Gift Box Campaigns**: Create and manage special gift box campaigns
- **Promotion System**: Advanced promotion management with multiple types

### 🛒 Shopping & Cart System
- **Dynamic Cart**: Real-time cart updates with AJAX
- **Quantity Management**: Add, remove, and update product quantities
- **Coupon System**: Apply discount codes (MarketVibe27, Shopping24/7)
- **Cart Persistence**: Cart data persists across sessions
- **Guest Cart**: Shopping cart functionality for non-authenticated users
- **Cart Summary**: Real-time calculation of subtotal, discount, tax, and total

### 💳 Payment & Order System
- **Multi-Vendor Payments**: Stripe Connect integration for direct seller payments
- **Payment Methods**: Support for Stripe and Cash on Delivery (COD)
- **Order Processing**: Complete order lifecycle management
- **Payment Tracking**: Real-time payment status updates
- **Webhook Integration**: Automated payment confirmation via Stripe webhooks
- **Order Status Tracking**: Pending, Processing, Shipped, Delivered, Cancelled states
- **Payment Records**: Complete payment transaction history

### 📦 Product Management
- **Dynamic Product Creation**: Category-based dynamic form generation
- **Product Categories**: Hierarchical category system with 8 main categories and 40 subcategories
- **Product Attributes**: Custom attributes per category (text, number, dropdown, boolean)
- **Product Images**: Multiple image support with thumbnail designation
- **Brand Management**: Product branding and logo support with 32+ popular brands
- **Product Conditions**: New, Used, Refurbished product states
- **Pricing System**: Base price, discount percentage, and final price calculation
- **Stock Management**: Real-time inventory tracking with low stock notifications
- **Product Reviews**: Customer rating and review system with like/dislike functionality

### 📊 Seller Dashboard
- **Overview Dashboard**: Sales statistics, recent orders, and key metrics
- **Order Management**: Complete order processing and tracking
- **Product Management**: Add, edit, delete, and list products
- **Sales Reports**: Revenue analytics with charts and graphs
- **Profile Management**: Edit seller profile and shop details
- **Promotion Management**: Create and manage product promotions
- **Data Export**: Export orders and products as CSV
- **Revenue Tracking**: Monitor earnings, payouts, and commission
- **Gift Box Management**: Manage gift box campaigns and orders
- **Notification System**: Real-time notifications for orders, stock, and payments

### 🎁 Gift Box Campaigns
- **Campaign Creation**: Sellers can create special gift box campaigns
- **Buyer Selection**: Buyers can choose products for gift boxes
- **Custom Messages**: Add personal messages to gift boxes
- **Reveal Options**: Choose whether to reveal gift box contents
- **Delivery Tracking**: Track gift box delivery status
- **Campaign Management**: Manage multiple gift box campaigns

### 🔧 Advanced Features
- **Dynamic Forms**: Category-based attribute forms for products
- **Image Processing**: Base64 encoding for efficient image storage and display
- **AJAX Integration**: Real-time updates without page refresh
- **Responsive Design**: Mobile-friendly interface with modern CSS
- **Search & Filter**: Product search and category filtering
- **Pagination**: Efficient data loading for large datasets
- **Error Handling**: Comprehensive error management and user feedback
- **Security**: CSRF protection, form validation, and secure data handling
- **Notification System**: Real-time notifications for buyers and sellers
- **Activity Tracking**: Complete activity logging for sellers

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication system
- **Payment Processing**: Stripe Connect API (v12.3.0)
- **File Storage**: Binary field storage for images (BLOB)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Charts**: Chart.js for analytics and reporting
- **Styling**: Custom CSS with modern gradient designs
- **AJAX**: Asynchronous data loading and updates
- **Image Processing**: Base64 encoding for efficient storage
- **Data Export**: CSV export functionality
- **Environment**: Python 3.8+ with virtual environment support

## 📁 Project Structure

```
MarketVibe/
├── MarketVibe/              # Main Django project settings
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── buyer/                   # Buyer app
│   ├── models.py            # Buyer, Cart, Order, Payment, GiftBoxOrder models
│   ├── views.py             # Buyer views and payment processing
│   ├── forms.py             # Buyer forms
│   ├── urls.py              # Buyer URL routing
│   ├── utils_order.py       # Order processing utilities
│   ├── context_processors.py # User sidebar data
│   └── templates/buyer/     # Buyer templates
│       ├── checkout_page.html
│       ├── cart_page.html
│       ├── buyer_profile.html
│       ├── buyer_dashboard.html
│       ├── giftbox_marketplace.html
│       ├── giftbox_orders.html
│       └── track_order.html
├── seller/                  # Seller app
│   ├── models.py            # Seller, Product, Category, Promotion models
│   ├── views.py             # Seller views and dashboard
│   ├── forms.py             # Seller and product forms
│   ├── urls.py              # Seller URL routing
│   ├── signals.py           # Django signals for notifications
│   ├── templatetags/        # Custom template tags
│   ├── management/          # Custom management commands
│   │   └── commands/
│   │       ├── populate_categories.py
│   │       ├── populate_brands.py
│   │       ├── populate_all_data.py
│   │       └── populate_activities_notifications.py
│   ├── static/seller/       # Static assets
│   │   ├── css/
│   │   └── js/
│   └── templates/seller/    # Seller templates
│       ├── seller_dashboard.html
│       ├── product_form.html
│       ├── product_list.html
│       ├── giftbox_campaigns.html
│       └── promotions_list.html
├── manage.py
├── requirements.txt
├── django_design_system.md  # Design system documentation
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Stripe account for payment processing

### Step 1: Clone the Repository
```bash
git clone https://github.com/BILALAKRAM27/ecommerce-fullstack-design.git
cd ecommerce-fullstack-design
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables
Create a `.env` file in the project root:
```env
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
STRIPE_CONNECT_CLIENT_ID=your_stripe_connect_client_id
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 7: Populate Sample Data (Recommended)
```bash
# Populate all data (categories, brands, etc.)
python manage.py populate_all_data

# Or run individual commands:
python manage.py populate_categories
python manage.py populate_brands
python manage.py populate_activities_notifications
```

### Step 8: Run Development Server
```bash
python manage.py runserver 8080
```

### Step 9: Start Stripe Webhook Listener (Development)
In a separate terminal:
```bash
stripe listen --forward-to localhost:8080/stripe/webhook/
```

Visit `http://localhost:8080/` to access the application.

## 📋 Usage

### Seller Registration & Setup
1. Navigate to `/register/`
2. Fill in seller information (name, email, shop details)
3. Upload profile image (optional)
4. Complete Stripe Connect onboarding at `/stripe/onboard/`
5. Access seller dashboard at `/dashboard/overview/`

### Seller Dashboard Features
- **Overview**: Sales statistics and recent activity
- **Orders**: Process and track customer orders
- **Products**: Manage product catalog and inventory
- **Reports**: View sales analytics and revenue reports
- **Profile**: Update seller information and shop details
- **Promotions**: Create and manage product promotions
- **Gift Boxes**: Manage gift box campaigns and orders
- **Export**: Download order and product data as CSV

### Buyer Shopping Experience
1. Register as a buyer at `/register/`
2. Browse products by category
3. Add items to cart with quantity selection
4. Apply coupon codes for discounts
5. Proceed to checkout with shipping address
6. Choose payment method (Stripe or COD)
7. Complete order and track delivery status

### Gift Box Campaigns
1. Sellers create gift box campaigns with fixed pricing
2. Buyers browse available gift box campaigns
3. Buyers select products for their gift box
4. Add personal messages and choose reveal options
5. Complete purchase and track delivery

### Payment Processing
- **Stripe Integration**: Secure online payments with card processing
- **Multi-Vendor Support**: Direct payments to sellers via Stripe Connect
- **Commission System**: Automatic platform commission calculation
- **Webhook Processing**: Real-time payment status updates
- **Payment Records**: Complete transaction history tracking

## 🔧 Configuration

### Database Configuration
The project uses SQLite by default. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Stripe Configuration
Configure Stripe settings in `settings.py`:

```python
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
STRIPE_CONNECT_CLIENT_ID = os.getenv('STRIPE_CONNECT_CLIENT_ID')
```

### Static Files
Configure static files for production:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📝 API Endpoints

### Authentication
- `POST /register/` - Seller/Buyer registration
- `POST /login/` - User login
- `POST /logout/` - User logout

### Buyer Endpoints
- `GET /buyer/profile/` - View buyer profile
- `POST /buyer/profile/update/` - Update buyer profile
- `POST /buyer/profile/delete/` - Delete buyer account
- `GET /buyer/cart/` - Get cart data
- `POST /buyer/cart/add/` - Add item to cart
- `POST /buyer/cart/remove/` - Remove item from cart
- `POST /buyer/cart/update/` - Update cart quantity
- `POST /buyer/cart/apply-coupon/` - Apply coupon code
- `GET /buyer/checkout/` - Checkout page
- `POST /buyer/place-order/` - Place COD order
- `POST /buyer/stripe/process-payment/` - Process Stripe payment
- `GET /buyer/gift-boxes/` - Browse gift box campaigns
- `POST /buyer/gift-boxes/buy/` - Purchase gift box

### Seller Endpoints
- `GET /seller/profile/` - View seller profile
- `POST /seller/profile/update/` - Update seller profile
- `POST /seller/profile/delete/` - Delete seller account
- `GET /seller/dashboard/overview/` - Seller dashboard
- `GET /seller/orders/list/` - Order management
- `GET /seller/products/list/` - Product management
- `POST /seller/products/add/` - Add new product
- `POST /seller/products/<id>/edit/` - Edit product
- `POST /seller/products/<id>/delete/` - Delete product
- `GET /seller/reports/` - Sales reports
- `POST /seller/promotions/create/` - Create promotion
- `GET /seller/giftbox-campaigns/` - Manage gift box campaigns
- `GET /seller/export/` - Export data

### Stripe Endpoints
- `POST /stripe/webhook/` - Stripe webhook processing
- `GET /stripe/onboard/` - Stripe Connect onboarding

## 🔒 Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Password Validation**: Minimum 8 characters with strength checking
- **Email Validation**: Proper email format validation
- **Session Security**: Secure session management
- **File Upload Security**: Validated file uploads
- **Stripe Security**: Secure payment processing with webhook verification
- **Input Validation**: Comprehensive client and server-side validation

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop and mobile
- **Modern Styling**: Gradient backgrounds and smooth animations
- **Form Validation**: Real-time client-side validation
- **Loading States**: Visual feedback during form submission
- **Error Handling**: Clear error messages and validation
- **Interactive Dashboard**: Real-time updates and charts
- **Professional Layout**: Card-based design for better organization
- **Image Preview**: Real-time image upload previews
- **Dark Mode Support**: Theme switching capability

## 💳 Payment Features

- **Stripe Connect**: Multi-vendor payment processing
- **Application Fees**: Automatic platform commission calculation
- **Direct Transfers**: Payments sent directly to seller accounts
- **Webhook Processing**: Real-time payment status updates
- **Payment Records**: Complete transaction history
- **Multiple Payment Methods**: Stripe and Cash on Delivery
- **Secure Processing**: PCI-compliant payment handling

## 📊 Analytics & Reporting

- **Sales Analytics**: Revenue tracking and reporting
- **Order Analytics**: Order processing statistics
- **Product Performance**: Product sales and popularity metrics
- **Customer Analytics**: Buyer behavior and preferences
- **Chart Visualization**: Interactive charts using Chart.js
- **Data Export**: CSV export functionality
- **Real-time Updates**: Live dashboard updates

## 🎁 Gift Box System

- **Campaign Management**: Sellers create gift box campaigns
- **Product Selection**: Buyers choose products for gift boxes
- **Custom Messages**: Personal messages for gift recipients
- **Reveal Options**: Choose to reveal or hide gift contents
- **Delivery Tracking**: Track gift box delivery status
- **Fixed Pricing**: Simplified pricing for gift boxes

## 🔔 Notification System

- **Real-time Notifications**: Instant updates for orders and payments
- **Email Notifications**: Automated email alerts
- **Dashboard Alerts**: Visual notification indicators
- **Activity Logging**: Complete activity tracking
- **Customizable Settings**: User preference management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Bilal Akram**
- GitHub: [@BILALAKRAM27](https://github.com/BILALAKRAM27)
- Email: bilalakram190204@gmail.com

## 🙏 Acknowledgments

- Django Documentation
- Stripe API Documentation
- Chart.js for data visualization
- Modern CSS techniques
- Bootstrap for inspiration

## 📞 Support

If you have any questions or need support, please open an issue on GitHub or contact the author.

---

**Note**: This is a development version. For production deployment, ensure proper security configurations, environment variables, and SSL certificates are set up. The Stripe webhook listener must be running in production for payment processing to work correctly. 