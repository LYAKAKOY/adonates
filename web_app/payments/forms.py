from django import forms


class DonateForm(forms.Form):
    nickname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'main__input'}))
    donated_sum = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2,
                                     widget=forms.TextInput(attrs={'class': 'main__input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'main__textarea'}), required=False)

    class Meta:
        fields = ['nickname', 'donated_sum', 'message']