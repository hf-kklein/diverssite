from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','visibility', 'pub_date', 'page')
    list_filter = ['pub_date','page','visibility']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
