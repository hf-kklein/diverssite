from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import Article, Category, Display, Image, File
from .forms import ArticleAdminForm


class FileTabularInline(admin.TabularInline):
    extra = 1


class FileInline(FileTabularInline):
    model = Article.files.through


class ImageInline(FileTabularInline):
    model = Article.images.through


@admin.register(Article)
class ArticleAdmin(SimpleHistoryAdmin):
    form = ArticleAdminForm
    inlines = [ImageInline, FileInline]
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "visibility",
        "pub_date",
    )
    list_filter = ["pub_date", "visibility", "show_on_pages"]
    search_fields = ["title"]
    exclude = ["images", "files"]


admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Display)
admin.site.register(File)
