from django.db.models import Sum
from django.http import HttpRequest
from config import settings
from payments.forms import DonateForm
from payments.models import PayoutModel, PaymentModel
from payments.yookassa_payment import YouKassaPayment
from payments.yookassa_payout import YouKassaPayout
from users.models import DonateModel, StreamerModel


def payout_logic(request: HttpRequest) -> str:
    donates = DonateModel.objects.filter(
        streamer__user=request.user).filter(withdrawn=False, payment__status='succeeded')
    balance = donates.aggregate(sum=Sum('payment__payment_sum'))['sum'] or 0
    if balance == 0:
        return 'balance is zero'
    payout_yoo = YouKassaPayout(settings.YOOKASSA_AGENT_ID, settings.YOOKASSA_PAYOUT_SECRET_KEY)
    payout = payout_yoo.create_payout_yookassa(balance, 41001614575714)
    for donate in donates:
        donate.withdrawn = True
        donate.save()
    PayoutModel.objects.create(payout_id=payout.id, payout_sum=payout.amount.value, status=payout.status,
                               streamer=request.user)
    return payout.status


def payment_logic(form: DonateForm, username: str) -> str:
    payment_yoo = YouKassaPayment(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
    payment = payment_yoo.create_payment(form.cleaned_data['donated_sum'], settings.YOOKASSA_REDIRECT_URL)
    PaymentModel.objects.create(payment_id=payment.id, payment_sum=payment.amount.value,
                                status=payment.status)
    DonateModel.objects.create(payment=PaymentModel.objects.get(payment_id=payment.id),
                               nickname=form.cleaned_data['nickname'], message=form.cleaned_data['message'],
                               streamer=StreamerModel.objects.get(user__username=username))

    return payment.id
