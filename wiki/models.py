from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return(self.name)

class Articles(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return(self.title)
    # visibility = models.CharField(choices=(("public","Public"),("members","Members")))
