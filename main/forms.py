from django import forms


'''Класс - форма для ввода логина и пароля'''
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        max_length=40,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )
