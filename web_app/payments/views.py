from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.response import Response

from config import settings
from .forms import DonateForm
from .yookassa_payment import YouKassaPayment
from .business_logic import payout_logic, payment_logic
from rest_framework.views import APIView


@csrf_exempt
def payment_confirm(request):
    payment_yoo = YouKassaPayment(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
    payment = payment_yoo.get_payment(request.GET.get('donate_id'))
    if payment.status == 'succeeded':
        return HttpResponseForbidden('Платеж успешно произведен')
    previous_redirect = request.META.get('HTTP_REFERER')
    return render(request, 'payments/html/confirm_donate.html', {'payment': payment,
                                                                 'previous_redirect': previous_redirect})


class PayoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payout_status = payout_logic(request)
        data = {
            'payout_status': payout_status
        }
        return Response(data)


# def payout_notification(request):
#     result = payout_logic(request)
#     if result:
#         request.session['notification'] = 'succeeded'
#         return redirect(reverse('withdraw'))
#     else:
#         request.session['notification'] = 'failed'
#         return redirect(reverse('withdraw'))


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

    return render(request, 'payments/html/donate.html', {'form': form, 'streamer': username})
