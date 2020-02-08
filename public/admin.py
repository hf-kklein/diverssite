from django.contrib import admin

# Register your models here.
from .models import Post

# class PostAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['title','text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     # list_display = ('question_text', 'pub_date', 'was_published_recently')
#     # list_filter = ['pub_date']
#     # search_fields = ['question_text']


admin.site.register(Post)
