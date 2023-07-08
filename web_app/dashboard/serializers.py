from rest_framework import serializers
from users.models import StreamerModel, DonateModel


class StreamerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamerModel
        fields = '__all__'


class DonateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonateModel
        fields = '__all__'
