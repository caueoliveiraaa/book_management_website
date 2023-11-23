from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    nameUser = forms.CharField(max_length=50)
    stock = forms.IntegerField()
    bill = forms.FloatField()
    is_superuser = forms.BooleanField(
        required=False,
        label="Is Admin",
        help_text="Admin User",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "nameUser",
            "stock",
            "bill",
            "is_superuser"
        ]