import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.shortcuts import render, redirect

from main.forms import LoginForm, AddNewsForm, AddAccountForm
from main.models import News, AccountInformation


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
    if request.method =='POST':
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
                NewAccount = AccountInformation(Login=Login, Name=Name, Surname=Surname, Patronymic=Patronymic, DateOfBirth=DateOfBirth, Grope=Groupe)
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
