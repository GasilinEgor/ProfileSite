from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from main.models import AccountInformation


def load():
    AccountInformation.objects.update()
    Pupils = AccountInformation.objects.filter(Grope='Ученик')
    Names = Pupils.values_list('Name', flat=True)
    Surnames = Pupils.values_list('Surname', flat=True)
    Patrinymics = Pupils.values_list("Patronymic", flat=True)
    Usernames = Pupils.values_list('Login', flat=True)
    pupils_list = []
    for i in range(len(Names)):
        pupils_list.append((f'Ученик_{i}', f'{Usernames[i]} {Names[i]} {Surnames[i]} {Patrinymics[i]}'))
    return pupils_list


def all_load():
    AccountInformation.objects.update()
    Pupils = AccountInformation.objects.all()
    Names = Pupils.values_list('Name', flat=True)
    Surnames = Pupils.values_list('Surname', flat=True)
    Patrinymics = Pupils.values_list("Patronymic", flat=True)
    Usernames = Pupils.values_list('Login', flat=True)
    pupils_list = []
    for i in range(len(Names)):
        pupils_list.append((f'Ученик_{i}', f'{Usernames[i]} {Names[i]} {Surnames[i]} {Patrinymics[i]}'))
    return pupils_list


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


class AddAccountForm(forms.Form):
    Login = forms.CharField(
        label='Логин',
        max_length=20,
        min_length=0,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Логин',
            }
        )
    )

    Password = forms.CharField(
        label='Пароль',
        max_length=40,
        min_length=0,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Пароль'
                   }
        )
    )

    Name = forms.CharField(
        label='Имя',
        max_length=20,
        min_length=0,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Имя'
                   }
        )
    )

    Surname = forms.CharField(
        label='Фамилия',
        max_length=100,
        min_length=0,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Фамилия'
                   }
        )
    )

    Patronymic = forms.CharField(
        label='Отчество',
        max_length=100,
        min_length=0,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Отчество'
                   }
        )
    )

    DateOfBirth = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(
            attrs={'placeholder': 'Дата рождения',
                   'type': 'date'
                   },
            format=['%d.%m.%Y']
        )
    )

    Choise = [('Учитель', 'Учитель'),
              ('Ученик', 'Ученик')]

    Groupe = forms.ChoiceField(choices=Choise, widget=forms.RadioSelect, label='Учитель или ученик')


class MakeKlasses(forms.Form):
    Name = forms.CharField(
        label='Наазвание группы',
        max_length=20,
        min_length=0,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Название группы',
                   }
        )
    )

    pupils = forms.MultipleChoiceField(choices=load(), required=False, widget=forms.CheckboxSelectMultiple)

    def set_choices(self, arr):
        self.fields['pupils'].choices = arr


class DeleteAccounts(forms.Form):
    pupils = forms.MultipleChoiceField(choices=all_load(), required=False, widget=forms.CheckboxSelectMultiple)

    def set_choices(self, arr):
        self.fields['pupils'].choices = arr