from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import DateInput


class CustomUserCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_superuser"
        ]
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Informe o nome do usuário'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Informe o primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Informe o último nome'
        self.fields['password1'].widget.attrs['placeholder'] = 'Informe a senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Informe a senha outra vez'


class BookCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    autor = forms.CharField(max_length=200, required=True)
    sinopse = forms.CharField(max_length=200, required=False)
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
            'autor',
            'sinopse',
            'data_lancamento',
        ]
