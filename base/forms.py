from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from .models import Message, Chat
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "placeholder": "Type your message..."}),
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
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "password"]

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class CreateChatForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    status = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[
            ("open", "Open"),
            ("close", "Close")
        ],
        initial="open"
    )
    
    class Meta:
        model = Chat
        fields = ["name", "description", "status"]
        exclude = ["host"]