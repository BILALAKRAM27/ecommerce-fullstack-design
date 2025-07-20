import base64
from django import forms
from .models import Buyer, Order, Payment, CartItem, Wishlist


class BuyerRegistrationForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Buyer
        fields = ['name', 'email', 'phone', 'address']

    def save(self, commit=True):
        buyer = super().save(commit=False)
        if self.cleaned_data.get('image'):
            image_file = self.cleaned_data['image']
            buyer.set_image(image_file.read())
        if commit:
            buyer.save()
        return buyer


class BuyerUpdateForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Buyer
        fields = ['name', 'email', 'phone', 'address']

    def save(self, commit=True):
        buyer = super().save(commit=False)
        if self.cleaned_data.get('image'):
            image_file = self.cleaned_data['image']
            buyer.set_image(image_file.read())
        if commit:
            buyer.save()
        return buyer


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']
