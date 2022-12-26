import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from simple_history.models import HistoricalRecords

# Create your models here.
from events.models import Event


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
    try:
        event = instance.event.name
        date = instance.event.date.strftime("%Y%m%d")
    except AttributeError:
        event = ""
        date = instance.date.strftime("%Y%m%d")

    title = "unnamed" if instance.title == "" else instance.title
    public = "public" if instance.public else "private"

    slug = slugify("-".join([type(instance).__name__, event, date, title]))

    similar_files = [i.file.name for i in Image.objects.all() if slug in i.file.name]

    slug = slug + "-" + str(len(similar_files))

    ext = filename.split(".")[-1]
    return f"{public}/wiki/{slug}.{ext}"


# https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django/34007383
# hier gehts weiter
class Image(models.Model):
    title = models.CharField(max_length=20, default=None, blank=True)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    file = models.ImageField(upload_to=file_directory_path, verbose_name="Image")
    public = models.BooleanField(default=False)
    # history = HistoricalRecords()

    def __str__(self):
        return os.path.basename(self.file.path)

    def image_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        if self.file and hasattr(self.file, "url"):
            return self.file.url
        else:
            return "/static/images/default_profile.png"


class File(models.Model):
    title = models.CharField(max_length=20, default=None, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    file = models.FileField(upload_to=file_directory_path, verbose_name="File")
    public = models.BooleanField(default=False)

    # history = HistoricalRecords()

    def __str__(self):
        return os.path.basename(self.file.path)

    def file_url(self):
        if self.file and hasattr(self.file, "url"):
            return self.file.url
        else:
            raise FileNotFoundError

    def file_type_icon(self):
        if self.file and hasattr(self.file, "url"):
            url = self.file.url
            if ".xlsx" in url or ".xls" in url:
                return "/static/images/excel.png"

            if ".docx" in url or ".doc" in url:
                return "/static/images/word.png"

            if ".pdf" in url:
                return "/static/images/pdf.png"

            else:
                return "/static/images/document.png"

        else:
            raise FileNotFoundError


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
