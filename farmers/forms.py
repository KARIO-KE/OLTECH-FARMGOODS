from django import forms
from .models import Product
from .models import Message
from django.contrib.auth.models import User


class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['farmer_name', 'short_message', 'full_message', 'image']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'text'}),
        }

    def clean_password(self):
        # Password can be left blank to keep the current password
        password = self.cleaned_data.get('password')
        if password == '':
            return None
        return password
