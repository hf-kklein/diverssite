from django.contrib import admin

# Register your models here.
from .models import Event, Location

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,    {'fields': ['name','category','date','location','description']}),
        ('info',  {'fields': ['author','visibility'],
                   'classes': ['collapse']}),
    ]

    list_display = ('name', 'category', 'date', 'location')
    list_filter = ['date','category','location']
    search_fields = ['name']



admin.site.register(Event, EventAdmin)

admin.site.register(Location)
