from django.db import models


class News(models.Model):
    Date = models.DateField()
    Author = models.CharField(max_length=40)
    Main = models.CharField(max_length=100)
    Text = models.CharField(max_length=2000)
    Tegs = models.CharField(max_length=300)