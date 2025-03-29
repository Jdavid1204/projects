from django import forms
from django.contrib.auth.forms import UserCreationForm
from api.models import CustomUser, Hobby


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password: forms.CharField = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "address@qmul.ac.uk"}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "date_of_birth", "password1", "password2"]