from django.contrib import admin
from .models import PaymentModel, PayoutModel


class PaymentAdmin(admin.ModelAdmin):
    search_fields = ['payment_id', ]


class PayoutAdmin(admin.ModelAdmin):
    search_fields = ['payout_id', ]


admin.site.register(PaymentModel, PaymentAdmin)
admin.site.register(PayoutModel, PayoutAdmin)
