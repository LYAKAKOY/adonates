from django.db import models
from django.contrib.auth.models import User
from payments.models import PaymentModel

type_card = [
    ('ЮMoney', 'ЮMoney'),
    ('Банковская карта', 'Банковская карта'),
    ('СБП', 'СБП')
]


class DonateModel(models.Model):
    payment = models.OneToOneField(PaymentModel, on_delete=models.PROTECT)
    nickname = models.CharField(verbose_name='Псевдоним', max_length=50)
    message = models.TextField(verbose_name='Сообщение доната', null=True, blank=True)
    streamer = models.ForeignKey('StreamerModel', related_name='streamer', on_delete=models.CASCADE)
    withdrawn = models.BooleanField(verbose_name='Выведено', default=False)

    def __str__(self):
        return f'{self.nickname}: {self.payment.payment_sum}'


class StreamerModel(models.Model):
    user = models.OneToOneField(User, related_name='user', verbose_name='Пользователь', on_delete=models.PROTECT)
    avatar = models.ImageField(verbose_name='Аватарка', default='default_profile_picture.png')
    balance = models.DecimalField(verbose_name='Общая сумма', max_digits=10, decimal_places=2, default=0)
    count_donations = models.IntegerField(verbose_name='Количество донатов', default=0)
    goal = models.DecimalField(verbose_name='Цель', max_digits=10, decimal_places=0, default=0.00)

    def __str__(self):
        return f'{self.user.username}'


class StreamerCard(models.Model):
    streamer = models.ForeignKey(StreamerModel, verbose_name='Стример', related_name='streamerCard',
                                 on_delete=models.PROTECT)
    type_payout = models.CharField(verbose_name='Способ вывода', choices=type_card, max_length=16)
    number_card = models.DecimalField(verbose_name='Номер карты', unique=True, max_digits=20, decimal_places=0)

    def __str__(self):
        return f'{self.streamer.user.username}: {self.type_payout}'