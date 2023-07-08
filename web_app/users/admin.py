from django.contrib import admin
from .models import StreamerModel, DonateModel, CardStreamer

# Register your models here.
admin.site.register(StreamerModel)
admin.site.register(DonateModel)
admin.site.register(CardStreamer)