from django.contrib import admin
from dashboard.models import ReaderMessages
from readers.models import Payment


class ReaderMessagesAdmin(admin.ModelAdmin):
    pass


class PaymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReaderMessages, ReaderMessagesAdmin)
admin.site.register(Payment, PaymentAdmin)
