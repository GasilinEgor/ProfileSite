import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.shortcuts import render, redirect

from main.forms import LoginForm, AddNewsForm, AddAccountForm, MakeKlasses, DeleteAccounts
from main.models import News, AccountInformation, Klass


def IndexPage(request):
    data = News.objects.all()
    context = {'News': data}
    return render(request, 'index.html', context)


def Login(request):
    if request.method == "post":
        log = LoginForm(request.POST)
        if log.is_valid():
            Username = log.data['username']
            Password = log.data['password']
            user = authenticate(request, username=Username, password=Password)
            if user is not None:
                login(request, user)
    return redirect('index')


def Logout(request):
    logout(request)
    return render(request, 'index.html', {})


def profile(request, name):
    try:
        user = User.objects.get(username=name)
        return render(request, 'index.html', {'user': user})
    except User.DoesNotExist:
        raise Http404


def AddNews(request):
    context = {}
    if request.method == 'POST':
        news = AddNewsForm(request.POST)
        if news.is_valid():
            date = datetime.date.today()
            author = news.data['Author']
            main = news.data['Main']
            text = news.data['Text']
            tegs = news.data['Tegs']
            NewNews = News(Date=date, Author=author, Main=main, Text=text, Tegs=tegs)
            NewNews.save()
            context['form'] = news
        else:
            context['form'] = news
    else:
        context['nothing_entered'] = True
        context['form'] = AddNewsForm()
    return render(request, 'AddNews.html', context)


def LoadAccountInformation(request):
    data = AccountInformation.objects.filter(request.user.username)
    context = {'information': data}
    return render(request, 'account.html', request)


def AddAccount(request):
    context = {}
    if request.method == 'POST':
        Account = AddAccountForm(request.POST)
        if Account.is_valid():
            IsOriginal = False
            Login = Account.data['Login']
            try:
                user = User.objects.get(username=Login)
            except:
                IsOriginal = True
            if (IsOriginal):
                Password = Account.data['Password']
                Name = Account.data['Name']
                Surname = Account.data['Surname']
                Patronymic = Account.data['Patronymic']
                DateOfBirth = Account.data['DateOfBirth']
                Groupe = Account.data['Groupe']
                NewAccount = AccountInformation(Login=Login, Name=Name, Surname=Surname, Patronymic=Patronymic,
                                                DateOfBirth=DateOfBirth, Grope=Groupe)
                NewAccount.save()
                NewUser = User.objects.create_user(username=Login, password=Password)
                NewUser.save()
                if Groupe == 'Учитель':
                    group = Group.objects.get(name='Учитель')
                else:
                    group = Group.objects.get(name='Ученик')
                group.user_set.add(NewUser)
                message = 'Аккаунт успешно создан!'
                context['message'] = message
                context['IsOriginal'] = IsOriginal
                context['form'] = Account
            else:
                message = 'Аккаунт с данным логином уже существует!'
                context['message'] = message
                context['IsOriginal'] = IsOriginal
                context['form'] = Account
        else:
            context['form'] = Account
    else:
        context['nothing_entered'] = True
        context['form'] = AddAccountForm()
    return render(request, "AddAccount.html", context)


def AdRedact(request):
    context = {'message': 'Выберите, что хотите отредактировать'}
    return render(request, 'AdminRedactor.html', context)


def NewKlasses(request):
    context = {}
    if request.method == 'POST':
        NewKlass = MakeKlasses(request.POST)
        if NewKlass.is_valid():
            select = NewKlass.cleaned_data['pupils']
            pupils = load()
            klass = Klass.objects.create(name=NewKlass.data['Name'], count=len(select))
            for i in range(len(select)):
                s = pupils[select[i]].split()
                klass.Pupils.add(AccountInformation.objects.filter(Login=s[0], Name=s[1], Surname=s[2], Patronymic=s[3]).first())
            klass.save()
            context['message'] = "Класс успешно создан!"
            context['form'] = MakeKlasses()
        else:
            context['message'] = "Есть ошибки"
            context['form'] = MakeKlasses()
    else:
        form = MakeKlasses()
        context['nothing_entered'] = True
        context['form'] = form
        context['message'] = 'Введите имя группы и выберите учеников, которые должны в нее входить'
    return render(request, 'MakeKlasses.html', context)


def load():
    AccountInformation.objects.update()
    Pupils = AccountInformation.objects.filter(Grope='Ученик')
    Names = Pupils.values_list('Name', flat=True)
    Surnames = Pupils.values_list('Surname', flat=True)
    Patrinymics = Pupils.values_list("Patronymic", flat=True)
    Usernames = Pupils.values_list('Login', flat=True)
    pupils_list = {}
    for i in range(len(Names)):
        pupils_list[f'Ученик_{i}'] = f'{Usernames[i]} {Names[i]} {Surnames[i]} {Patrinymics[i]}'
    return pupils_list


def all_load():
    AccountInformation.objects.update()
    Pupils = AccountInformation.objects.all()
    Names = Pupils.values_list('Name', flat=True)
    Surnames = Pupils.values_list('Surname', flat=True)
    Patrinymics = Pupils.values_list("Patronymic", flat=True)
    Usernames = Pupils.values_list('Login', flat=True)
    pupils_list = {}
    for i in range(len(Names)):
        pupils_list[f'Ученик_{i}'] = f'{Usernames[i]} {Names[i]} {Surnames[i]} {Patrinymics[i]}'
    return pupils_list


def deleting(request):
    context = {}
    if request.method == 'POST':
        all_accounts = DeleteAccounts(request.POST)
        if all_accounts.is_valid():
            select = all_accounts.cleaned_data['pupils']
            print(select)
            pupils = all_load()
            print(pupils[select[0]])
            for i in range(len(select)):
                s = pupils[select[i]].split()
                try:
                    user = User.objects.get(username=s[0])
                    user.delete()
                    AccountInformation.objects.filter(Login=s[0], Name=s[1], Surname=s[2], Patronymic=s[3]).delete()
                except:
                    print("Ошибка! Данный аккаунт уже не существует!")
            context['message'] = "Успешно удалено!"
            context['form'] = DeleteAccounts()
        else:
            context['message'] = "Есть ошибки"
            context['form'] = DeleteAccounts()
    else:
        form = DeleteAccounts()
        context['nothing_entered'] = True
        context['form'] = form
        context['message'] = 'Выберите аккаунты, которые хотите удалить'
    return render(request, 'DeleteAccounts.html', context)