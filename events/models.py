from django.conf import settings
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Categ(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return self.name


# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    categ = models.ForeignKey(Categ, null=True, on_delete=models.PROTECT)
    date = models.DateTimeField()
    description = MarkdownxField(null=True, blank=True)
    location = models.ForeignKey("Location", on_delete=models.PROTECT, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    visibility = models.CharField(max_length=20, default="public")
    slug = models.SlugField(max_length=50, null=True, editable=False)

    @property
    def formatted_markdown(self):
        return markdownify(self.description)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name + str(self.date)
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class PartChoice(models.Model):
    choice = models.CharField(max_length=1)
    choicetext = models.CharField(max_length=20)

    def __str__(self):
        return self.choicetext


class Participation(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    part = models.ForeignKey("PartChoice", on_delete=models.PROTECT, related_name="party", null=True)

    def __str__(self):
        return str(self.id)
