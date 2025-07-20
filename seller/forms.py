import base64
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Seller, Product, ProductImage, Brand, Category


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


class SellerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
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
    class Meta:
        model = Product
        fields = [
            'category', 'brand', 'name', 'description',
            'base_price', 'discount_percentage', 'final_price',
            'stock', 'condition'
        ]


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image_url', 'is_primary']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo_url']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'description', 'icon_url']
