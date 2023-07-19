from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StreamerModel
from .tasks import recount_total_sum, recount_sum_goal
from payments.models import PaymentModel
from .models import DonateModel, StreamerSettings, StreamerGoal


@receiver(post_save, sender=User)
def create_streamer_account(sender: User, instance: User, created: bool, **kwargs) -> None:
    if created:
        streamer = StreamerModel()
        streamer.user = instance
        streamer.save()


@receiver(post_save, sender=StreamerModel)
def create_streamer_account(sender: User, instance: StreamerModel, created: bool, **kwargs) -> None:
    if created:
        streamer_settings = StreamerSettings()
        streamer_settings.streamer = instance
        streamer_settings.save()
        streamer_goal = StreamerGoal()
        streamer_goal.streamer = instance
        streamer_goal.save()


@receiver(post_save, sender=PaymentModel)
def recalc_balance(sender, instance: PaymentModel, created: bool, **kwargs) -> None:
    if DonateModel.objects.filter(payment=instance).exists():
        recount_total_sum.delay(instance.pk)


@receiver(pre_save, sender=StreamerGoal)
def change_goal(sender, instance: StreamerGoal, **kwargs) -> None:
    if instance.pk and instance.goal != StreamerGoal.objects.get(pk=instance.pk).goal:
        instance.sum_goal = 0


@receiver(post_save, sender=PaymentModel)
def recalc_goal_sum(sender, instance: PaymentModel, created: bool, **kwargs) -> None:
    if DonateModel.objects.filter(payment=instance).exists() and \
            int(StreamerGoal.objects.get(streamer=DonateModel.objects.get(payment=instance).streamer).goal) != 0:
        recount_sum_goal.delay(instance.pk)
