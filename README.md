# MarketVibe - Multi-Vendor E-commerce Platform

A comprehensive multi-vendor e-commerce platform built with Django 5.2.4, featuring advanced seller/buyer management, Stripe Connect payment processing, dynamic product catalog, gift box campaigns, smart search system, and robust order management system.

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

### 🔍 Smart Search System
- **Real-time Search**: Dynamic product search with instant suggestions
- **Multi-field Search**: Search by product name, ID, or description
- **Category Filtering**: Filter search results by product category
- **Search Suggestions**: Dropdown with product images, names, and prices
- **Keyboard Navigation**: Full keyboard support for accessibility
- **Debounced Search**: Optimized performance with 300ms delay
- **Mobile Responsive**: Touch-friendly search interface

### 🎠 Hero Carousel
- **Dynamic Product Showcase**: Rotating carousel with real product images
- **Category Slides**: Electronics, Furniture, Sports, and Clothing categories
- **Auto-play Functionality**: Automatic rotation every 5 seconds
- **Manual Navigation**: Previous/Next buttons and indicator dots
- **Responsive Design**: Optimized for all screen sizes
- **Keyboard Support**: Arrow keys and accessibility features
- **Hover Pause**: Auto-play pauses on hover for better UX

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
- **Additional Libraries**: 
  - pandas (2.3.0) for data processing
  - openpyxl (3.1.2) for Excel export
  - reportlab (4.1.0) for PDF generation
  - matplotlib (3.10.3) for data visualization
  - numpy (1.26.4) for numerical operations

## 📁 Project Structure

```
MarketVibe/
├── MarketVibe/                    # Main Django project settings
│   ├── __init__.py
│   ├── settings.py                # Project configuration
│   ├── urls.py                    # Main URL routing
│   ├── wsgi.py                    # WSGI configuration
│   └── asgi.py                    # ASGI configuration
├── buyer/                         # Buyer app
│   ├── __init__.py
│   ├── admin.py                   # Buyer admin interface
│   ├── apps.py                    # Buyer app configuration
│   ├── models.py                  # Buyer, Cart, Order, Payment, GiftBoxOrder models
│   ├── views.py                   # Buyer views and payment processing (2803 lines)
│   ├── forms.py                   # Buyer forms
│   ├── urls.py                    # Buyer URL routing
│   ├── utils_order.py             # Order processing utilities
│   ├── utils.py                   # Utility functions
│   ├── context_processors.py      # User sidebar data
│   ├── tests.py                   # Buyer app tests
│   ├── migrations/                # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── 0003_cart_coupon_code_alter_cartitem_quantity.py
│   │   ├── 0004_remove_buyer_address_address.py
│   │   ├── 0005_alter_order_options_order_notes_and_more.py
│   │   ├── 0006_order_order_type.py
│   │   ├── 0007_buyernotification.py
│   │   ├── 0008_giftboxorder.py
│   │   ├── 0009_giftboxorder_delivery_address.py
│   │   ├── 0010_buyer_address_buyer_date_of_birth_buyer_updated_at_and_more.py
│   │   ├── 0011_giftboxorder_expected_delivery_date_and_more.py
│   │   ├── 0012_giftboxorder_order_type_giftboxorder_payment_status.py
│   │   └── 0013_giftboxorder_promotion_order_promotion.py
│   └── templates/buyer/           # Buyer templates
│       ├── buyer_dashboard.html
│       ├── buyer_profile.html
│       ├── buyer_seller_profile_view.html
│       ├── buyer_order_list.html
│       ├── cart_page.html
│       ├── checkout_page.html
│       ├── contact_support.html
│       ├── giftbox_marketplace.html
│       ├── giftbox_orders.html
│       ├── order_details.html
│       ├── track_order.html
│       ├── buy_giftbox.html
│       ├── buyer_delete.html
│       └── buyer_update.html
├── seller/                        # Seller app
│   ├── __init__.py
│   ├── admin.py                   # Seller admin interface
│   ├── apps.py                    # Seller app configuration
│   ├── models.py                  # Seller, Product, Category, Promotion models (415 lines)
│   ├── views.py                   # Seller views and dashboard (3672 lines)
│   ├── forms.py                   # Seller and product forms (315 lines)
│   ├── urls.py                    # Seller URL routing (103 lines)
│   ├── signals.py                 # Django signals for notifications (122 lines)
│   ├── tests.py                   # Seller app tests
│   ├── migrations/                # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_seller_user.py
│   │   ├── 0003_alter_seller_image.py
│   │   ├── 0004_product_image_product_order_count.py
│   │   ├── 0005_remove_productimage_image_url_product_unique_id_and_more.py
│   │   ├── 0006_rename_is_primary_productimage_is_thumbnail_and_more.py
│   │   ├── 0007_seller_stripe_account_id.py
│   │   ├── 0008_seller_address.py
│   │   ├── 0009_notification.py
│   │   ├── 0010_activity.py
│   │   ├── 0011_promotion.py
│   │   ├── 0012_giftboxcampaign_sellergiftboxparticipation.py
│   │   ├── 0013_alter_productreview_options_productreview_updated_at_and_more.py
│   │   └── 0014_sellerreview_rating.py
│   ├── templatetags/              # Custom template tags
│   │   └── b64filters.py         # Base64 image filters
│   ├── management/                # Custom management commands
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── README.md          # Commands documentation
│   │       ├── populate_all_data.py
│   │       ├── populate_brands.py
│   │       ├── populate_categories.py
│   │       ├── populate_categories_legacy.py
│   │       ├── populate_comprehensive_categories.py
│   │       ├── populate_dashboard_data.py
│   │       ├── populate_activities_notifications.py
│   │       ├── populate_buyer_notifications.py
│   │       ├── populate_attribute_options.py
│   │       └── fix_promotions.py
│   ├── static/seller/             # Static assets
│   │   ├── assets/
│   │   │   ├── icon.png
│   │   │   ├── icons8-gift.gif
│   │   │   ├── stripe.png
│   │   │   └── web-main.jpg
│   │   ├── css/
│   │   │   └── index.css
│   │   └── js/
│   │       └── index.js
│   └── templates/seller/          # Seller templates
│       ├── index.html             # Main homepage with carousel
│       ├── seller_dashboard.html
│       ├── product_form.html
│       ├── product_list.html
│       ├── product_page.html
│       ├── ecom_product_listing.html
│       ├── giftbox_campaigns.html
│       ├── giftbox_orders.html
│       ├── fulfill_giftbox_order.html
│       ├── hot_offers.html
│       ├── orders_list.html
│       ├── promotions_list.html
│       ├── create_promotion.html
│       ├── promotion_detail.html
│       ├── products_list.html
│       ├── seller_profile.html
│       ├── login.html
│       ├── register.html
│       ├── about.html
│       ├── find_store.html
│       ├── partnership.html
│       ├── information.html
│       ├── money_refund.html
│       ├── shipping.html
│       └── contact_support.html
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── django_design_system.md       # Design system documentation
├── db.sqlite3                    # SQLite database (3.3MB)
├── .gitignore                    # Git ignore rules
├── fix_promotions.py             # Promotion fix script
├── fix_category_attributes.py    # Category attributes fix script
├── test_ajax.py                  # AJAX testing script
├── test_export_comprehensive.py  # Export testing script
├── test_export_functionality.py  # Export functionality tests
└── test_total_spent.py          # Total spent calculation tests
```

## 🚀 Installation & Setup

### Prerequisites
- **Python**: 3.8 or higher
- **pip**: Python package installer
- **Git**: Version control system
- **Stripe Account**: For payment processing (optional for development)

### Step 1: Clone the Repository
```bash
git clone https://github.com/BILALAKRAM27/ecommerce-fullstack-design.git
cd ecommerce-fullstack-design
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Environment Variables Setup
Create a `.env` file in the project root:
```env
# Stripe Configuration (Required for payment processing)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret
STRIPE_CONNECT_CLIENT_ID=ca_your_stripe_connect_client_id

# Django Configuration (Optional - defaults provided)
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Database Setup
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to database
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
python manage.py populate_buyer_notifications
python manage.py populate_attribute_options
```

### Step 8: Run Development Server
```bash
# Start Django development server
python manage.py runserver 8080
```

### Step 9: Start Stripe Webhook Listener (Development)
In a separate terminal:
```bash
# Install Stripe CLI (if not already installed)
# Download from: https://stripe.com/docs/stripe-cli

# Start webhook listener
stripe listen --forward-to localhost:8080/stripe/webhook/
```

### Step 10: Access the Application
- **Main Application**: http://localhost:8080/
- **Admin Interface**: http://localhost:8080/admin/
- **Seller Dashboard**: http://localhost:8080/dashboard/overview/
- **Buyer Dashboard**: http://localhost:8080/buyer/dashboard/

## 🔧 Configuration

### Database Configuration
The project uses SQLite by default. For production, update `MarketVibe/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'marketvibe_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Stripe Configuration
Configure Stripe settings in `MarketVibe/settings.py`:

```python
# Stripe API Keys
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
STRIPE_CONNECT_CLIENT_ID = os.getenv('STRIPE_CONNECT_CLIENT_ID')
```

### Static Files Configuration
For production deployment:

```python
# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Email Configuration (Optional)
For email notifications, add to `settings.py`:

```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

## 📋 Usage Examples

### Seller Registration & Setup
1. **Navigate to Registration**: Go to `http://localhost:8080/register/`
2. **Fill Seller Information**: 
   - Name: "John's Electronics"
   - Email: "john@example.com"
   - Shop Description: "Premium electronics and gadgets"
3. **Upload Profile Image**: Optional profile picture
4. **Complete Stripe Onboarding**: Visit `/stripe/onboard/` to set up payments
5. **Access Dashboard**: Go to `/dashboard/overview/` for seller dashboard

### Buyer Shopping Experience
1. **Register as Buyer**: Go to `http://localhost:8080/register/`
2. **Browse Products**: Use the smart search or category navigation
3. **Add to Cart**: Click "Add to Cart" on any product
4. **Apply Coupons**: Use codes like "MarketVibe27" or "Shopping24/7"
5. **Checkout**: Proceed to checkout with shipping address
6. **Payment**: Choose Stripe or Cash on Delivery
7. **Track Order**: Monitor delivery status in buyer dashboard

### Gift Box Campaigns
1. **Seller Creates Campaign**: 
   - Go to `/giftbox-campaigns/`
   - Set fixed price and product selection
2. **Buyer Browses**: 
   - Visit `/buyer/gift-boxes/`
   - Choose from available campaigns
3. **Customize Gift Box**:
   - Select products for the gift box
   - Add personal message
   - Choose reveal options
4. **Complete Purchase**: Checkout and track delivery

### Smart Search Usage
1. **Search by Name**: Type product names in the search bar
2. **Search by ID**: Enter product unique ID
3. **Category Filter**: Select category before searching
4. **Real-time Suggestions**: See instant product suggestions
5. **Keyboard Navigation**: Use arrow keys to navigate suggestions

## 🧪 Testing

### Run Test Suite
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test buyer
python manage.py test seller

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Scripts
```bash
# Test AJAX functionality
python test_ajax.py

# Test export functionality
python test_export_comprehensive.py
python test_export_functionality.py

# Test total spent calculations
python test_total_spent.py
```

### Manual Testing Checklist
- [ ] User registration (buyer/seller)
- [ ] Login/logout functionality
- [ ] Product search and filtering
- [ ] Cart operations (add/remove/update)
- [ ] Checkout process
- [ ] Payment processing (Stripe/COD)
- [ ] Order management
- [ ] Seller dashboard features
- [ ] Gift box campaigns
- [ ] Responsive design (mobile/desktop)

## 📝 API Endpoints

### 🔐 Authentication Endpoints
- `POST /register/` - Seller/Buyer registration
- `POST /login/` - User login with email/password
- `POST /logout/` - User logout and session cleanup

### 🛍️ Buyer Endpoints
#### Profile Management
- `GET /buyer/profile/` - View buyer profile
- `POST /buyer/profile/update/` - Update buyer information
- `POST /buyer/profile/delete/` - Delete buyer account
- `GET /buyer/dashboard/` - Buyer dashboard overview

#### Shopping Cart
- `GET /cart/` - Get current cart data
- `POST /cart/add/` - Add item to cart
- `POST /cart/remove/` - Remove item from cart
- `POST /cart/update/` - Update cart quantity
- `POST /cart/apply-coupon/` - Apply discount coupon
- `POST /cart/clear/` - Clear entire cart
- `GET /cart/page/` - Cart page view
- `POST /cart/check/` - Check cart status

#### Wishlist Management
- `POST /wishlist/add/` - Add product to wishlist
- `POST /wishlist/remove/` - Remove from wishlist
- `POST /wishlist/check/` - Check wishlist status

#### Checkout & Orders
- `GET /checkout/` - Checkout page
- `POST /place-order/` - Place COD order
- `POST /stripe/process-payment/` - Process Stripe payment
- `GET /orders/<id>/` - Order details
- `GET /orders/<id>/track/` - Track order status
- `GET /buyer_orders/` - Buyer order list

#### Gift Box System
- `GET /gift-boxes/` - Browse gift box campaigns
- `GET /gift-boxes/buy/<seller_id>/<campaign_id>/` - Purchase gift box
- `GET /gift-boxes/orders/` - Gift box orders

#### Notifications
- `POST /notification/mark-read/` - Mark notification as read
- `POST /notification/mark-all-read/` - Mark all notifications as read
- `POST /notification/clear-all/` - Clear all notifications

### 🏪 Seller Endpoints
#### Profile Management
- `GET /profile/` - View seller profile
- `POST /profile/update/` - Update seller profile
- `POST /profile/delete/` - Delete seller account
- `GET /profile/edit/` - Edit profile page

#### Dashboard & Analytics
- `GET /dashboard/` - Seller dashboard overview
- `GET /orders/` - Order management
- `GET /revenue/` - Revenue tracking
- `GET /reports/` - Sales reports
- `GET /stripe/status/` - Stripe Connect status

#### Product Management
- `GET /products/list/` - Product listing
- `POST /products/create/` - Create new product
- `GET /products/<id>/` - Product details
- `POST /products/<id>/update/` - Update product
- `POST /products/<id>/delete/` - Delete product
- `POST /products/<id>/duplicate/` - Duplicate product

#### Order Management
- `GET /orders/list/` - Order listing
- `GET /order/<id>/details/` - Order details
- `POST /order/update-status/` - Update order status

#### Promotion System
- `GET /promotions/` - Promotion listing
- `POST /promotions/create/` - Create promotion
- `GET /promotion/<id>/` - Promotion details
- `POST /promotion/<id>/delete/` - Delete promotion
- `POST /promotion/<id>/update/` - Update promotion

#### Gift Box Management
- `GET /giftbox-campaigns/` - Manage gift box campaigns
- `POST /giftbox-campaigns/join/<id>/` - Join campaign
- `GET /giftbox-orders/` - Gift box orders
- `POST /giftbox-orders/fulfill/<id>/` - Fulfill gift box order

#### Review System
- `POST /products/<id>/review/` - Submit product review
- `POST /seller/<id>/review/` - Submit seller review
- `POST /reviews/<type>/<id>/like/` - Like/dislike review
- `GET /products/<id>/reviews/` - Get product reviews
- `GET /seller/<id>/reviews/` - Get seller reviews

#### AJAX Endpoints
- `POST /ajax/get-category-children/` - Get subcategories
- `POST /ajax/get-category-attributes/` - Get category attributes
- `POST /ajax/save-attribute-value/` - Save attribute values
- `POST /ajax/get-filtered-products/` - Filter products
- `POST /search-suggestions/` - Search suggestions
- `POST /check-new-orders/` - Check for new orders
- `POST /check-low-stock/` - Check low stock alerts

#### Export & Data
- `GET /export/` - Export data
- `POST /export-data/` - Export data AJAX
- `GET /test-export/` - Test export functionality

### 💳 Stripe Integration
- `POST /stripe/webhook/` - Stripe webhook processing
- `GET /stripe/onboard/` - Stripe Connect onboarding

### 📄 Static Pages
- `GET /about/` - About Us page
- `GET /find-store/` - Find Store page
- `GET /partnership/` - Partnership page
- `GET /information/` - Information page
- `GET /money-refund/` - Money Refund policy
- `GET /shipping/` - Shipping policy

## 🔒 Security Features

### 🛡️ Authentication & Authorization
- **CSRF Protection**: All forms include CSRF tokens
- **Session Security**: Secure session management with timeout
- **Password Validation**: Minimum 8 characters with strength checking
- **Email Validation**: Proper email format validation
- **Account Lockout**: Protection against brute force attacks

### 🔐 Data Protection
- **Input Validation**: Comprehensive client and server-side validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Content Security Policy headers
- **File Upload Security**: Validated file uploads with type checking
- **Data Encryption**: Sensitive data encryption at rest

### 💳 Payment Security
- **Stripe Security**: PCI-compliant payment processing
- **Webhook Verification**: Secure webhook signature verification
- **Payment Tokenization**: Secure payment token handling
- **Fraud Detection**: Basic fraud prevention measures

### 🚫 Access Control
- **Role-based Access**: Separate buyer and seller permissions
- **Profile Privacy**: Protected user information
- **Admin Controls**: Secure admin interface access
- **API Rate Limiting**: Protection against abuse

## 🎨 UI/UX Features

### 📱 Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Tablet Support**: Responsive tablet layouts
- **Desktop Experience**: Full-featured desktop interface
- **Cross-Browser**: Compatible with all modern browsers

### 🎨 Visual Design
- **Modern Gradients**: Beautiful gradient backgrounds
- **Smooth Animations**: CSS transitions and animations
- **Professional Layout**: Card-based design system
- **Consistent Typography**: Unified font hierarchy
- **Color Scheme**: Cohesive color palette

### 🔍 Smart Search System
- **Real-time Suggestions**: Instant search results
- **Keyboard Navigation**: Full keyboard support
- **Category Filtering**: Filter by product category
- **Debounced Search**: Performance optimization
- **Mobile Touch**: Touch-friendly interface

### 🎠 Hero Carousel
- **Auto-play Functionality**: Automatic slide rotation
- **Manual Navigation**: Previous/Next buttons
- **Indicator Dots**: Visual slide indicators
- **Hover Pause**: User-friendly interaction
- **Responsive Images**: Optimized for all screen sizes

### 📊 Interactive Dashboard
- **Real-time Updates**: Live data updates
- **Chart Visualization**: Interactive charts with Chart.js
- **Data Export**: CSV export functionality
- **Notification System**: Real-time alerts
- **Activity Logging**: Complete activity tracking

### 🛒 Shopping Experience
- **Dynamic Cart**: Real-time cart updates
- **Wishlist Management**: Save favorite products
- **Coupon System**: Discount code application
- **Progress Indicators**: Visual checkout progress
- **Order Tracking**: Real-time order status

### 🔔 Notification System
- **Real-time Alerts**: Instant notifications
- **Email Notifications**: Automated email alerts
- **Dashboard Indicators**: Visual notification badges
- **Customizable Settings**: User preference management
- **Activity Feed**: Complete activity history

## 💳 Payment Features

### 💳 Stripe Integration
- **Multi-Vendor Payments**: Direct seller payments via Stripe Connect
- **Application Fees**: Automatic platform commission calculation
- **Secure Processing**: PCI-compliant payment handling
- **Webhook Processing**: Real-time payment status updates
- **Payment Records**: Complete transaction history

### 💰 Payment Methods
- **Credit/Debit Cards**: Secure card processing
- **Cash on Delivery**: COD payment option
- **Multiple Currencies**: Support for different currencies
- **Payment Plans**: Flexible payment options

### 🔄 Payment Flow
- **Order Creation**: Secure order processing
- **Payment Authorization**: Real-time payment verification
- **Fund Transfer**: Direct transfer to seller accounts
- **Refund Processing**: Automated refund handling
- **Dispute Resolution**: Payment dispute management

## 📊 Analytics & Reporting

### 📈 Sales Analytics
- **Revenue Tracking**: Real-time revenue monitoring
- **Order Analytics**: Order processing statistics
- **Product Performance**: Product sales metrics
- **Customer Analytics**: Buyer behavior analysis
- **Trend Analysis**: Sales trend identification

### 📊 Dashboard Metrics
- **Key Performance Indicators**: Important business metrics
- **Real-time Charts**: Interactive data visualization
- **Export Capabilities**: Data export functionality
- **Custom Reports**: Flexible reporting options
- **Historical Data**: Long-term trend analysis

### 📋 Data Export
- **CSV Export**: Comma-separated value exports
- **Excel Export**: Spreadsheet format exports
- **PDF Reports**: Professional PDF reports
- **Custom Formats**: Flexible export options
- **Scheduled Exports**: Automated data exports

## 🎁 Gift Box System

### 🎯 Campaign Management
- **Campaign Creation**: Sellers create gift box campaigns
- **Fixed Pricing**: Simplified pricing structure
- **Product Selection**: Curated product collections
- **Campaign Analytics**: Performance tracking
- **Inventory Management**: Stock level monitoring

### 🛍️ Buyer Experience
- **Campaign Browsing**: Browse available campaigns
- **Product Selection**: Choose products for gift boxes
- **Custom Messages**: Personal message addition
- **Reveal Options**: Choose content visibility
- **Delivery Tracking**: Track gift box delivery

### 📦 Order Fulfillment
- **Order Processing**: Automated order handling
- **Fulfillment Tracking**: Real-time fulfillment status
- **Quality Control**: Order verification process
- **Shipping Management**: Delivery coordination
- **Customer Support**: Gift box support system

## 🔔 Notification System

### 📱 Real-time Notifications
- **Instant Updates**: Real-time notification delivery
- **Multiple Channels**: Email, dashboard, and in-app notifications
- **Customizable Alerts**: User preference management
- **Priority Levels**: Important vs. informational notifications
- **Read Status**: Track notification engagement

### 📧 Email Notifications
- **Order Confirmations**: Purchase confirmation emails
- **Shipping Updates**: Delivery status notifications
- **Payment Receipts**: Payment confirmation emails
- **Promotional Offers**: Marketing email campaigns
- **Account Alerts**: Security and account notifications

### 📊 Dashboard Alerts
- **Visual Indicators**: Notification badges and icons
- **Activity Feed**: Complete activity history
- **Quick Actions**: One-click notification actions
- **Filtering Options**: Notification organization
- **Bulk Operations**: Mass notification management

## 🤝 Contributing

### 📋 Development Guidelines
1. **Fork the Repository**: Create your own fork
2. **Create Feature Branch**: `git checkout -b feature/AmazingFeature`
3. **Follow Code Style**: Use consistent formatting and naming
4. **Write Tests**: Include tests for new features
5. **Update Documentation**: Keep README and docs current
6. **Commit Changes**: Use descriptive commit messages
7. **Push to Branch**: `git push origin feature/AmazingFeature`
8. **Open Pull Request**: Submit for review

### 🧪 Testing Requirements
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Ensure optimal performance
- **Security Tests**: Verify security measures

### 📝 Code Standards
- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use consistent ES6+ syntax
- **HTML/CSS**: Follow semantic markup principles
- **Documentation**: Include docstrings and comments
- **Git**: Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**MIT License Features:**
- ✅ Commercial use allowed
- ✅ Modification permitted
- ✅ Distribution allowed
- ✅ Private use allowed
- ✅ No liability
- ✅ No warranty

## 👨‍💻 Author

**Bilal Akram**
- **GitHub**: [@BILALAKRAM27](https://github.com/BILALAKRAM27)
- **Email**: bilalakram190204@gmail.com
- **LinkedIn**: [Bilal Akram](https://linkedin.com/in/bilal-akram)
- **Portfolio**: [Personal Website](https://bilalakram.dev)

**About the Developer:**
- Full-stack web developer with expertise in Django and modern web technologies
- Passionate about creating user-friendly e-commerce solutions
- Committed to open-source development and community contribution
- Experienced in payment processing and security implementation

## 🙏 Acknowledgments

### 🛠️ Technologies & Libraries
- **Django**: Web framework and documentation
- **Stripe**: Payment processing API and documentation
- **Chart.js**: Data visualization library
- **Font Awesome**: Icon library
- **Bootstrap**: CSS framework inspiration

### 📚 Learning Resources
- **Django Documentation**: Official Django docs
- **Stripe API Documentation**: Payment processing guides
- **Modern CSS Techniques**: Advanced styling methods
- **Web Security Best Practices**: Security implementation
- **E-commerce Design Patterns**: User experience insights

### 🎨 Design Inspiration
- **Modern E-commerce Platforms**: Amazon, Shopify, WooCommerce
- **Material Design**: Google's design system
- **Apple's Design Language**: Clean and intuitive interfaces
- **Responsive Design Principles**: Mobile-first approach
- **Accessibility Guidelines**: WCAG compliance standards

## 📞 Support & Community

### 🆘 Getting Help
- **GitHub Issues**: Report bugs and request features
- **Email Support**: Direct contact for urgent issues
- **Documentation**: Comprehensive setup and usage guides
- **Community Forum**: Developer community discussions

### 🔧 Troubleshooting
- **Common Issues**: Frequently encountered problems
- **Setup Problems**: Installation and configuration issues
- **Payment Issues**: Stripe integration problems
- **Performance Issues**: Optimization and scaling
- **Security Concerns**: Security-related questions

### 📈 Feature Requests
- **New Features**: Suggest new functionality
- **Improvements**: Enhance existing features
- **Bug Reports**: Report software issues
- **Documentation**: Improve project documentation
- **Testing**: Contribute to test coverage

## 🚀 Deployment

### 🌐 Production Deployment
- **Environment Variables**: Secure configuration management
- **Database Setup**: PostgreSQL production database
- **Static Files**: Configure static file serving
- **SSL Certificate**: HTTPS encryption setup
- **Domain Configuration**: Custom domain setup

### 🔧 Server Requirements
- **Python**: 3.8 or higher
- **PostgreSQL**: Production database
- **Redis**: Caching and session storage
- **Nginx**: Web server and reverse proxy
- **SSL Certificate**: HTTPS encryption

### 📊 Monitoring & Maintenance
- **Error Tracking**: Monitor application errors
- **Performance Monitoring**: Track system performance
- **Security Updates**: Regular security patches
- **Backup Strategy**: Data backup procedures
- **Scaling Strategy**: Handle increased traffic

---

**Note**: This is a development version. For production deployment, ensure proper security configurations, environment variables, and SSL certificates are set up. The Stripe webhook listener must be running in production for payment processing to work correctly.

**Version**: 2.0.0  
**Last Updated**: January 2025  
**Django Version**: 5.2.4  
**Python Version**: 3.8+  
**License**: MIT License 