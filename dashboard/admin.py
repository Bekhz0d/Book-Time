from django.contrib import admin
from dashboard.models import ReaderMessages


class ReaderMessagesAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReaderMessages, ReaderMessagesAdmin)
