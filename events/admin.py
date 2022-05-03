from django.contrib import admin

# Register your models here.
from .models import Event, Location, PartChoice, Participation, Categ


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "categ", "date", "location", "visibility"]}),
        (
            "info",
            {
                "fields": [
                    "description",
                ],
                "classes": ["collapse"],
            },
        ),
    ]

    list_display = ("name", "date", "location")
    list_filter = ["date", "location"]
    search_fields = ["name"]


class CategAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "person", "part")
    list_filter = ["event", "person", "part"]
    verbose_name_plural = "participation"


admin.site.register(Event, EventAdmin)

admin.site.register(Location, LocationAdmin)

admin.site.register(PartChoice)
admin.site.register(Categ, CategAdmin)

admin.site.register(Participation, ParticipationAdmin)
