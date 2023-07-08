from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import PayoutModel
from users.models import StreamerModel


@receiver(post_save, sender=PayoutModel)
def set_balance_zero(sender, instance: PayoutModel, created: bool, **kwargs) -> None:
    if created and instance.status == 'succeeded':
        streamer = StreamerModel.objects.get(user=instance.streamer)
        streamer.balance = 0.00
        streamer.save()