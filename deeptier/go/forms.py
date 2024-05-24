from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    referral_code = forms.CharField(max_length=20, required=False, help_text="Enter referral code if you have one")

    class Meta:
        model = CustomUser
        fields = ['uid', 'phone_number', 'password', 'company_name', 'entity_type']
