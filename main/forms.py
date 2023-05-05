from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

'''Класс - форма для ввода логина и пароля'''


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Логин"),
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': _("Имя"),
                   }
        )
    )
    password = forms.CharField(
        label='Пароль',
        max_length=40,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Пароль'
                   }
        )
    )


class AddNewsForm(forms.Form):
    Author = forms.CharField(
        label='Автор',
        max_length=40,
        min_length=0,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    Main = forms.CharField(
        label='Загаловок',
        max_length=100,
        min_length=0,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    Text = forms.CharField(
        label='Основной текст',
        max_length=2000,
        min_length=0,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    Tegs = forms.CharField(
        label='Теги',
        max_length=300,
        min_length=0,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )