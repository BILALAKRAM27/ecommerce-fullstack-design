import base64
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Seller, Product, ProductImage, Brand, Category
from buyer.models import Buyer
from .models import CategoryAttribute, ProductAttributeValue


class SellerLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    user_type = forms.ChoiceField(
        choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
        widget=forms.RadioSelect,
        initial='buyer'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()  # Hide username field
        self.fields['username'].required = False

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_type = self.cleaned_data.get('user_type')

        if email and password:
            # Try to find user by email
            try:
                user = User.objects.get(email=email)
                self.user_cache = user
                # Set username for authentication
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')
            
            # Check if user is a seller when seller type is selected
            if user_type == 'seller':
                try:
                    seller = Seller.objects.get(user=user)
                except Seller.DoesNotExist:
                    raise forms.ValidationError('This email is not registered as a seller.')
            
            # Authenticate user
            if not self.user_cache.check_password(password):
                raise forms.ValidationError('Invalid email or password.')

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
        widget=forms.RadioSelect,
        initial='buyer'
    )
    phone = forms.CharField(max_length=20, required=False)
    shop_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SellerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    user_type = forms.ChoiceField(
        choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
        widget=forms.RadioSelect,
        initial='buyer'
    )
    image = forms.FileField(required=False)

    class Meta:
        model = Seller
        fields = ['name', 'email', 'shop_name', 'shop_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make shop_name and shop_description optional initially
        self.fields['shop_name'].required = False
        self.fields['shop_description'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        user_type = cleaned_data.get('user_type')
        shop_name = cleaned_data.get('shop_name')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        if user_type == 'seller' and not shop_name:
            raise forms.ValidationError("Shop name is required for sellers")

        return cleaned_data

    def save(self, commit=True):
        seller = super().save(commit=False)
        if self.cleaned_data.get('image'):
            image_file = self.cleaned_data['image']
            seller.set_image(image_file.read())
        if commit:
            seller.save()
        return seller


class SellerUpdateForm(forms.ModelForm):
    image = forms.FileField(required=False)
    email = forms.EmailField(disabled=True, required=False)  # Make email read-only

    class Meta:
        model = Seller
        fields = ['name', 'email', 'shop_name', 'shop_description', 'image']

    def save(self, commit=True):
        seller = super().save(commit=False)
        # Don't update the email field
        seller.email = self.instance.email  # Keep the original email
        if self.cleaned_data.get('image'):
            image_file = self.cleaned_data['image']
            seller.set_image(image_file.read())
        if commit:
            seller.save()
        return seller


class ProductForm(forms.ModelForm):
    image = forms.FileField(required=False, label="Product Image")
    
    class Meta:
        model = Product
        fields = [
            'category', 'brand', 'name', 'description',
            'base_price', 'discount_percentage', 'final_price',
            'stock', 'condition'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'base_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'discount_percentage': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'final_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        
        # Handle image upload
        if self.cleaned_data.get('image'):
            image_file = self.cleaned_data['image']
            product.set_image(image_file.read())
        
        # Calculate final price if discount is provided
        if product.discount_percentage and product.base_price:
            product.final_price = product.base_price * (1 - product.discount_percentage / 100)
        
        if commit:
            product.save()
        return product


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image_url', 'is_primary']
        widgets = {
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }


class DynamicProductForm(forms.ModelForm):
    image = forms.FileField(required=False, label="Product Image")
    
    class Meta:
        model = Product
        fields = [
            'category', 'brand', 'name', 'description',
            'base_price', 'discount_percentage', 'final_price',
            'stock', 'condition'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'base_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'discount_percentage': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'final_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category field hidden initially
        self.fields['category'].widget = forms.HiddenInput()

    def save(self, commit=True):
        product = super().save(commit=False)
        
        # Handle image upload
        if self.cleaned_data.get('image'):
            image_file = self.cleaned_data['image']
            product.set_image(image_file.read())
        
        # Calculate final price if discount is provided
        if product.discount_percentage and product.base_price:
            product.final_price = product.base_price * (1 - product.discount_percentage / 100)
        
        if commit:
            product.save()
            
            # Handle dynamic attributes
            self.save_dynamic_attributes(product)
        
        return product

    def save_dynamic_attributes(self, product):
        """Save dynamic attributes from form data"""
        for field_name, value in self.data.items():
            if field_name.startswith('attribute_') and value:
                attribute_id = field_name.replace('attribute_', '')
                try:
                    attribute = CategoryAttribute.objects.get(id=attribute_id)
                    ProductAttributeValue.objects.create(
                        product=product,
                        attribute=attribute,
                        value=value
                    )
                except CategoryAttribute.DoesNotExist:
                    pass


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo_url']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'description', 'icon_url']
