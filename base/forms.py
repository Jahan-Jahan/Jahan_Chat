from django import forms
from django.forms import ModelForm
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your message...'}),
        }

class RegisterForm(UserCreationForm):
    username = forms.CharField (
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField (
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "password"]
