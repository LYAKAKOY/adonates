# Generated by Django 4.2.1 on 2023-07-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_streamersettings_sum_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamercard',
            name='default_payout',
            field=models.BooleanField(default=True, verbose_name='Выбранный способ вывода'),
        ),
    ]