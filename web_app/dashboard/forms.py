from django import forms
from users.models import StreamerModel, StreamerSettings


class ChangeProfileForm(forms.Form):
    username = forms.CharField()
    avatar = forms.ImageField()

    class Meta:
        model = StreamerModel
        fields = ['username', 'avatar']


class ChangeSettingsForm(forms.Form):
    goal = forms.DecimalField()
    min_sum_donate = forms.DecimalField()

    class Meta:
        model = StreamerSettings
        fields = ['goal', 'min_sum_donate']