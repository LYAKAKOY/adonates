from django.contrib import admin
from .models import PaymentModel, PayoutModel

admin.site.register(PaymentModel)
admin.site.register(PayoutModel)
