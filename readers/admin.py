from django.contrib import admin
from main.models import Readers


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'balance', 'status', 'address')
    search_fields = ('usename', 'first_name', 'last_name', 'email', 'address', 'phone')


admin.site.register(Readers, ReaderAdmin)
