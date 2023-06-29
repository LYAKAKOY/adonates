from django.contrib import admin
from .models import StreamerModel, DonateModel

# Register your models here.
admin.site.register(StreamerModel)
admin.site.register(DonateModel)
