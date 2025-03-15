from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('agent', 'Agent'),
    ]
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']
