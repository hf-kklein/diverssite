from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Info


class InfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Info, SimpleHistoryAdmin)
