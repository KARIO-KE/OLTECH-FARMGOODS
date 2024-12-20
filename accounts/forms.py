from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('farmer', 'Farmer'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "role"]


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    is_buyer = forms.BooleanField(required=False)
    is_farmer = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_buyer', 'is_farmer']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Automatically handle user approval based on whether they are a farmer
        if user.is_farmer:
            user.is_approved = False  # Set to False, requires admin approval

        return user


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


class ProfilePhotoForm(forms.Form):
    photo = forms.ImageField(label='Profile Photo', required=True)
