from django import forms
from payments.business_logic import type_card


class PayoutAddForm(forms.Form):
    type_payout = forms.ChoiceField(choices=type_card, initial='ЮMoney', widget=forms.Select(
        attrs={'class': 'selection', 'onchange': 'findOption(this)', 'size': '1'}))
    number_card = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'max-cash inp_cash', 'placeholder': '201831893',
        'style': 'border: 1px solid rgba(255, 255, 255, 1);', 'step': 'any'}))

    class Meta:
        fields = ['payout_type', 'number_card']
