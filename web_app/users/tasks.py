from celery import shared_task
from celery_singleton import Singleton
from django.db.models import Sum
from payments.models import PaymentModel
from .models import StreamerModel, DonateModel


@shared_task
def recount_sum_goal(donate_pk: PaymentModel.pk):
    donate = DonateModel.objects.get(payment__pk=donate_pk)
    streamer = StreamerModel.objects.get(user=donate.streamer.user)
    if donate.payment.status == 'succeeded':
        streamer.streamerSettings.sum_goal += donate.payment.payment_sum
        streamer.streamerSettings.save()


@shared_task(base=Singleton)
def recount_total_sum(donate_pk: PaymentModel.pk):
    streamer = StreamerModel.objects.get(user=DonateModel.objects.get(payment__pk=donate_pk).streamer.user)
    donates_related_to_streamer = DonateModel.objects.filter(
        streamer=streamer, payment__status='succeeded', withdrawn=False)
    streamer.balance = donates_related_to_streamer.aggregate(sum=Sum('payment__payment_sum'))['sum'] or 0.00
    streamer.count_donations = donates_related_to_streamer.count()
    streamer.save()
