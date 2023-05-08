from django.db import models
from django.contrib.auth.models import Group


class News(models.Model):
    Date = models.DateField()
    Author = models.CharField(max_length=40)
    Main = models.CharField(max_length=100)
    Text = models.CharField(max_length=2000)
    Tegs = models.CharField(max_length=300)


class AccountInformation(models.Model):
    Login = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    Surname = models.CharField(max_length=100)
    Patronymic = models.CharField(max_length=100)
    DateOfBirth = models.DateField()
    Grope = models.CharField(max_length=255, default='none')
