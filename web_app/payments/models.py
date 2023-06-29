from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class PaymentModel(models.Model):
    payment_id = models.CharField(verbose_name='Платеж', primary_key=True, max_length=50, editable=False)
    payment_sum = models.DecimalField(verbose_name='Сумма платежа', max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(verbose_name='Дата платежа', default=now)
    status = models.CharField(verbose_name='Статус платежа', max_length=15)

    def __str__(self):
        return f'{self.payment_sum}: {self.status}'


class PayoutModel(models.Model):
    payout_id = models.CharField(verbose_name='Выплата', primary_key=True, max_length=50, editable=False)
    payout_sum = models.DecimalField(verbose_name='Сумма выплаты', max_digits=10, decimal_places=2)
    payout_date = models.DateTimeField(verbose_name='Дата выплаты', default=now)
    status = models.CharField(verbose_name='Статус выплаты')
    streamer = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.streamer.username}: {self.payout_sum}'
