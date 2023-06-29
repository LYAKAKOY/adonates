from celery import shared_task
from django.utils import timezone
from users.models import PaymentModel
from yookassa import Configuration, Payment
from users.models import DonateModel
from config import settings


@shared_task
def set_canceled_payment():
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    pending_payments = PaymentModel.objects.filter(status='pending')
    for payment in pending_payments:
        if (timezone.now() - payment.payment_date).seconds > 1800 and Payment.find_one(
                payment_id=payment.payment_id).captured_at:
            Payment.cancel(payment.payment_id)
        elif (timezone.now() - payment.payment_date).seconds > 1800:
            payment.status = 'canceled'
            payment.save()


@shared_task
def delete_canceled_payment():
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    canceled_payments = PaymentModel.objects.filter(status='canceled')
    for payment in canceled_payments:
        DonateModel.objects.get(payment=payment).delete()
        payment.delete()


@shared_task
def check_payment_status():
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    pending_payments = PaymentModel.objects.filter(status='pending')
    for payment in pending_payments:
        payment_status = Payment.find_one(payment_id=payment.payment_id).status
        if payment_status != payment.status:
            payment.status = payment_status
            payment.save()