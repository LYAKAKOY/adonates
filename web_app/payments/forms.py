from django import forms
from config.settings import TYPE_CARD


class DonateForm(forms.Form):
    nickname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'main__input'}))
    donated_sum = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2,
                                     widget=forms.TextInput(attrs={'class': 'main__input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'main__textarea'}), required=False)

    class Meta:
        fields = ['nickname', 'donated_sum', 'message']


class PayoutAddForm(forms.Form):
    type_payout = forms.ChoiceField(choices=TYPE_CARD, initial='ЮMoney', widget=forms.Select(
        attrs={'class': 'selection', 'onchange': 'findOption(this)', 'size': '1'}))
    number_card = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'max-cash inp_cash', 'placeholder': '201831893',
        'style': 'border: 1px solid rgba(255, 255, 255, 1);', 'step': 'any'}))

    class Meta:
        fields = ['payout_type', 'number_card']
