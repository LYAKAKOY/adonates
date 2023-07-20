from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from config import settings
from .forms import DonateForm, PayoutAddForm
from .yookassa_payment import YouKassaPayment
from .business_logic import payment_logic
from users.models import StreamerModel, StreamerCard


@csrf_exempt
def payment_confirm(request):
    payment_yoo = YouKassaPayment(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
    payment = payment_yoo.get_payment(request.GET.get('donate_id'))
    if payment.status == 'succeeded':
        return HttpResponseForbidden('Платеж успешно произведен')
    previous_redirect = request.META.get('HTTP_REFERER')
    return render(request, 'payments/html/confirm_donate.html', {'payment': payment,
                                                                 'previous_redirect': previous_redirect})


@login_required
def create_payout_method(request):
    if request.method == 'POST':
        form = PayoutAddForm(request.POST)
        if form.is_valid():
            if StreamerCard.objects.filter(streamer__user=request.user, type_payout=form.cleaned_data['type_payout']).exists():
                streamer_card = StreamerCard.objects.get(streamer__user=request.user,
                                                         type_payout=form.cleaned_data['type_payout'])
                streamer_card.number_card = form.cleaned_data['number_card']
                streamer_card.save()
                return redirect(reverse('withdraw'))

            StreamerCard.objects.create(streamer=StreamerModel.objects.get(user=request.user),
                                        type_payout=form.cleaned_data['type_payout'],
                                        number_card=form.cleaned_data['number_card'])

    return redirect(reverse('withdraw'))


def addDonate(request, username):
    request.session['person'] = request.session.session_key
    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            try:
                payment_id = payment_logic(form, username)
                return redirect(reverse('payment_confirm') + f'?donate_id={payment_id}')
            except Exception as e:
                form.add_error(None, e)
    else:
        form = DonateForm()

    return render(request, 'payments/html/donate.html', {'form': form,
                                                         'streamer': StreamerModel.objects.get(
                                                             user__username=username)})
