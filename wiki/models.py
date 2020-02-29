from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return(self.name)

class Articles(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    text = MarkdownxField()
    pub_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=50)

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def __str__(self):
        return(self.title)
    # visibility = models.CharField(choices=(("public","Public"),("members","Members")))
