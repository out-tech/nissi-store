from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SpecialOrder, Review, Order

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SpecialOrderForm(forms.ModelForm):
    class Meta:
        model = SpecialOrder
        fields = ['name', 'phone', 'whatsapp', 'fabric', 'size', 'budget', 'design_details', 'image']
        widgets = {
            'design_details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe how you want your cloth designed...'}),
            'fabric': forms.TextInput(attrs={'placeholder': 'e.g. Kente, Ankara, Lace'}),
            'size': forms.TextInput(attrs={'placeholder': 'e.g. Size 10, Medium'}),
            'budget': forms.TextInput(attrs={'placeholder': 'e.g. GH₵ 500'}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'payment_method', 'payment_reference']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'payment_reference': forms.TextInput(attrs={'placeholder': 'MoMo Transaction ID / Paystack Ref (if paid)'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell others about this product...'}),
        }