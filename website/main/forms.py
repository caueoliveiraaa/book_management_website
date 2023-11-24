from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import DateInput


class CustomUserCreationForm(UserCreationForm):
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
            "first_name",
            "last_name",
            "password1",
            "password2",
            "bill",
            "is_superuser"
        ]


class BookCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    author = forms.CharField(max_length=200, required=True)
    synopsis = forms.CharField(max_length=200, required=False)
    data_lancamento = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        widget=DateInput(attrs={'type': 'date'}),
        help_text='Enter the date in DD-MM-YYYY format or pick from the calendar.',
    )

    class Meta:
        model = Books
        fields = [
            'name',
            'author',
            'synopsis',
            'data_lancamento',
        ]
