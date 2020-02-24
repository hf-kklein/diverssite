from django.db import models

# Create your models here.

class Category(models.Model):
    name =models.CharField(max_length=50)

class Articles(models.Model):
    category = models.(max_length=50)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # visibility = models.CharField(choices=(("public","Public"),("members","Members")))
