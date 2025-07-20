# MarketVibe - Django E-commerce Platform

A full-stack e-commerce platform built with Django, featuring user authentication, seller/buyer management, and product catalog functionality.

## 🚀 Features

### Authentication & User Management
- **Dual User Types**: Separate registration for Buyers and Sellers
- **Secure Login**: Email-based authentication with password validation
- **Profile Management**: User profiles with image upload support
- **Account Deletion**: Complete account removal (both User and Seller records)

### Seller Features
- **Seller Registration**: Complete seller onboarding process
- **Profile Management**: Update seller information and shop details
- **Image Upload**: Profile image storage as BLOB in database
- **Shop Management**: Shop name, description, and rating system

### Buyer Features
- **Buyer Registration**: Simple buyer account creation
- **Profile Management**: Basic buyer profile functionality

### Security Features
- **CSRF Protection**: Built-in Django CSRF token validation
- **Form Validation**: Comprehensive client and server-side validation
- **Password Security**: Password strength checking and confirmation
- **Session Management**: Secure login/logout functionality

## 🛠️ Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication system
- **File Storage**: Binary field storage for images
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with modern gradient designs

## 📁 Project Structure

```
MarketVibe/
├── MarketVibe/          # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── seller/              # Seller app
│   ├── models.py        # Seller, Product, Category models
│   ├── views.py         # Authentication and CRUD views
│   ├── forms.py         # Custom forms for registration/update
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
│       └── seller/
│           ├── register.html
│           ├── login.html
│           ├── seller_profile.html
│           ├── seller_update.html
│           └── seller_delete.html
├── buyer/               # Buyer app (future development)
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

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

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 📋 Usage

### Seller Registration
1. Navigate to `/sellers/register/`
2. Fill in seller information (name, email, shop details)
3. Upload profile image (optional)
4. Submit to create seller account

### Seller Login
1. Go to `/sellers/login/`
2. Enter email and password
3. Select "Seller" user type
4. Access seller dashboard

### Buyer Registration
1. Navigate to `/sellers/register/`
2. Fill in buyer information
3. Select "Buyer" user type
4. Complete registration

### Profile Management
- **View Profile**: `/sellers/profile/`
- **Update Profile**: `/sellers/profile/update/`
- **Delete Account**: `/sellers/profile/delete/`
- **Logout**: Available in profile page

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
- `POST /sellers/register/` - Seller/Buyer registration
- `POST /sellers/login/` - User login
- `POST /sellers/logout/` - User logout

### Seller Management
- `GET /sellers/profile/` - View seller profile
- `POST /sellers/profile/update/` - Update seller profile
- `POST /sellers/profile/delete/` - Delete seller account

## 🔒 Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Password Validation**: Minimum 8 characters with strength checking
- **Email Validation**: Proper email format validation
- **Session Security**: Secure session management
- **File Upload Security**: Validated file uploads

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop and mobile
- **Modern Styling**: Gradient backgrounds and smooth animations
- **Form Validation**: Real-time client-side validation
- **Loading States**: Visual feedback during form submission
- **Error Handling**: Clear error messages and validation

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
- Django REST Framework
- Bootstrap for inspiration
- Modern CSS techniques

## 📞 Support

If you have any questions or need support, please open an issue on GitHub or contact the author.

---

**Note**: This is a development version. For production deployment, ensure proper security configurations and environment variables are set up. 