from django.conf import settings
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from simple_history.models import HistoricalRecords

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Display(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


vis_choice = (("public", "Public"), ("members", "Members"))


def file_directory_path(instance, filename):
    slug = slugify("-".join([
        type(instance).__name__, 
        instance.title,
        instance.date.strftime("%Y%m%d") + 
        instance.time.strftime("%H%M%S%f")
    ]))
    ext = filename.split(".")[-1]
    return f"wiki/{slug}.{ext}"


# https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django/34007383
# hier gehts weiter
class Image(models.Model):
    title = models.CharField(max_length=20, default=None, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    image = models.ImageField(upload_to=file_directory_path, verbose_name="Image")
    # history = HistoricalRecords()


class File(models.Model):
    title = models.CharField(max_length=20, default=None, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    file = models.FileField(upload_to=file_directory_path, verbose_name="File")
    # history = HistoricalRecords()


class Article(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    text = MarkdownxField()
    pub_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=50)
    visibility = models.CharField(max_length=20, default="public", choices=vis_choice)
    show_on_pages = models.ManyToManyField(Display)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    history = HistoricalRecords()
    files = models.ManyToManyField(File, default=None, blank=True)
    images = models.ManyToManyField(Image, default=None, blank=True)

    # Create your models here.

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def __str__(self):
        return self.title
