from django.shortcuts import render, redirect
from main.forms import LoginForm
from django.http import Http404, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User


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


def profile(request, name):
    try:
        user = User.objects.get(username=name)
        return render(request, 'index.html', {'user': user})
    except User.DoesNotExist:
        raise Http404
