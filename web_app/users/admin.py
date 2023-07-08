from django.contrib import admin
from .models import StreamerModel, DonateModel, StreamerCard

# Register your models here.
admin.site.register(StreamerModel)
admin.site.register(DonateModel)
admin.site.register(StreamerCard)