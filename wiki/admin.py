from django.contrib import admin
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import Article, Category, Display


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
