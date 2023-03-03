import datetime

from django.shortcuts import render, redirect
from main.forms import LoginForm, AddNewsForm
from django.http import Http404, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from main.models import News


def IndexPage(request):
    return render(request, 'index.html', {})


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