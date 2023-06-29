from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StreamerModel
from .tasks import recount_total_sum
from payments.models import PaymentModel
from .models import DonateModel


@receiver(post_save, sender=User)
def create_donation_account(sender: User, instance: User, created: bool, **kwargs) -> None:
    if created:
        donation_account = StreamerModel()
        donation_account.user = instance
        donation_account.save()

