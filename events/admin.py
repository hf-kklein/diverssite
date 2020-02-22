from django.contrib import admin

# Register your models here.
from .models import Event, Location, PartChoice, Participation

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,    {'fields': ['name','category','date','location','description']}),
        ('info',  {'fields': ['author','visibility'],
                   'classes': ['collapse']}),
    ]

    list_display = ('name', 'category', 'date', 'location')
    list_filter = ['date','category','location']
    search_fields = ['name']



class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'person', 'part')
    list_filter = ['event', 'person', 'part']

admin.site.register(Event, EventAdmin)

admin.site.register(Location)

admin.site.register(PartChoice)

admin.site.register(Participation, ParticipationAdmin)
