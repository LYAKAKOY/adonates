from django import forms
from .models import StreamerModel, StreamerSettings, StreamerGoal


class ChangeProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=False)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'avatar', 'name': 'image', 'id': 'image'}),
                              required=False)

    class Meta:
        model = StreamerModel
        fields = ['username', 'avatar']


class ChangeGoalForm(forms.ModelForm):
    goal = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2, required=False)
    description = forms.CharField(max_length=250, required=False)

    class Meta:
        model = StreamerGoal
        fields = ['goal', 'description']


class ChangeSettingsForm(forms.ModelForm):
    min_sum_donate = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = StreamerSettings
        fields = ['min_sum_donate']
