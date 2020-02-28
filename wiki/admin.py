from django.contrib import admin

# Register your models here.
from .models import Category, Articles

class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(Category)
admin.site.register(Articles, ArticlesAdmin)
