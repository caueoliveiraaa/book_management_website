from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import DateInput


class CustomUserCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField(
        required=False,
        label="É usuário administrado "
    )

    bill = forms.FloatField(
        label="Multa",
        initial=0.0,
        widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
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
        help_text='Formato DD-MM-YYYY.',
    )

    class Meta:
        model = Books
        fields = [
            'name',
            'author',
            'synopsis',
            'data_lancamento',
        ]
