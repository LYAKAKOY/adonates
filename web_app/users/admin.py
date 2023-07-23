from django.contrib import admin
from .models import StreamerModel, DonateModel, StreamerCard, StreamerSettings, StreamerGoal


class StreamerAdmin(admin.ModelAdmin):
    search_fields = ['user__username', ]


class StreamerCardAdmin(admin.ModelAdmin):
    search_fields = ['streamer__user__username', ]


admin.site.register(StreamerModel, StreamerAdmin)
admin.site.register(DonateModel)
admin.site.register(StreamerCard, StreamerCardAdmin)
admin.site.register(StreamerSettings)
admin.site.register(StreamerGoal)
