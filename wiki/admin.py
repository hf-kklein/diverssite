from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.forms.widgets import CheckboxSelectMultiple
from django.db import models


# Register your models here.
from .models import Category, Article, Display


class ArticleAdmin(SimpleHistoryAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "visibility", "pub_date")
    list_filter = ["pub_date", "visibility", "show_on_pages"]
    search_fields = ["title"]

    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Display)
