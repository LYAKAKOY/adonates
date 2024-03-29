from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from payments.models import PaymentModel
from config.settings import TYPE_CARD


class DonateModel(models.Model):
    payment = models.OneToOneField(PaymentModel, related_name='donate', on_delete=models.PROTECT)
    nickname = models.CharField(verbose_name='Псевдоним', max_length=50)
    message = models.TextField(verbose_name='Сообщение доната', null=True, blank=True)
    streamer = models.ForeignKey('StreamerModel', related_name='streamer', on_delete=models.CASCADE)
    withdrawn = models.BooleanField(verbose_name='Выведено', default=False)

    def __str__(self):
        return f'{self.nickname}: {self.payment.payment_sum}'

    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'
        ordering = ['nickname']


class StreamerModel(models.Model):
    user = models.OneToOneField(User, related_name='user', verbose_name='Пользователь', on_delete=models.PROTECT)
    avatar = models.ImageField(verbose_name='Аватарка', default='default_profile_picture.png')
    balance = models.DecimalField(verbose_name='Общая сумма', max_digits=10, decimal_places=2, default=0)
    count_donations = models.IntegerField(verbose_name='Количество донатов', default=0)

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.avatar.path)

        if image.height > 150 and image.width > 150:
            image.thumbnail((150, 150))
            image.save(self.avatar.path)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Стример'
        verbose_name_plural = 'Стримеры'


class StreamerGoal(models.Model):
    streamer = models.OneToOneField(StreamerModel, verbose_name='Стример', related_name='streamerGoal',
                                    on_delete=models.CASCADE)
    sum_goal = models.DecimalField(verbose_name='Сумма цели', max_digits=10, decimal_places=2, default=0.00)
    goal = models.DecimalField(verbose_name='Цель', max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(verbose_name='Описание', max_length=200, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.streamer.user.username}: {self.goal}'

    class Meta:
        verbose_name = 'Цель стримера'
        verbose_name_plural = 'Цели стримеров'


class StreamerSettings(models.Model):
    streamer = models.OneToOneField(StreamerModel, verbose_name='Стример', related_name='streamerSettings',
                                    on_delete=models.CASCADE)
    min_sum_donate = models.DecimalField(verbose_name='Минимальная сумма доната',
                                         max_digits=10, decimal_places=2, default=1.00)

    def __str__(self):
        return f'{self.streamer.user.username}'

    class Meta:
        verbose_name = 'Настройки стримера'
        verbose_name_plural = 'Настройки стримеров'


class StreamerCard(models.Model):
    streamer = models.ForeignKey(StreamerModel, verbose_name='Стример', related_name='streamerCard',
                                 on_delete=models.CASCADE)
    type_payout = models.CharField(verbose_name='Способ вывода', choices=TYPE_CARD, max_length=16)
    number_card = models.DecimalField(verbose_name='Номер карты', unique=True, max_digits=20, decimal_places=0)
    default_payout = models.BooleanField(verbose_name='Выбранный способ вывода', default=False)

    def __str__(self):
        return f'{self.streamer.user.username}: {self.type_payout}'

    class Meta:
        verbose_name = 'Способ вывода'
        verbose_name_plural = 'Способы вывода'
