from django.contrib import admin

# Register your models here.
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "E-Mail",
            {
                "fields": [
                    "sender",
                    "recipients",
                    "subject",
                    "body",
                ]
            },
        )
    ]

    list_display = ("subject", "sender", "timestamp")
    list_filter = ["sender"]
    search_fields = ["timestamp"]
    # prepopulated_fields = {"slug": ("name","date")}


admin.site.register(Message, MessageAdmin)
