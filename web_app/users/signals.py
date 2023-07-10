from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StreamerModel
from .tasks import recount_total_sum
from payments.models import PaymentModel
from .models import DonateModel, StreamerSettings


@receiver(post_save, sender=User)
def create_streamer_account(sender: User, instance: User, created: bool, **kwargs) -> None:
    if created:
        streamer = StreamerModel()
        streamer.user = instance
        streamer.save()
        streamer_settings = StreamerSettings()
        streamer_settings.streamer = streamer
        streamer_settings.save()


@receiver(post_save, sender=DonateModel)
def recalc_balance(sender, instance: DonateModel, created: bool, **kwargs) -> None:
    if created:
        recount_total_sum.delay(instance.payment.pk)


@receiver(post_save, sender=PaymentModel)
def recalc_balance(sender, instance: PaymentModel, created: bool, **kwargs) -> None:
    if DonateModel.objects.filter(payment=instance).exists():
        recount_total_sum.delay(instance.pk)
