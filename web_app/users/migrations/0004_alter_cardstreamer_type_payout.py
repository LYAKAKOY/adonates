# Generated by Django 4.2.1 on 2023-07-08 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_cardstreamer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardstreamer',
            name='type_payout',
            field=models.CharField(choices=[('ЮMoney', 'ЮMoney'), ('Банковская карта', 'Банковская карта'), ('СБП', 'СБП')], max_length=16, verbose_name='Способ вывода'),
        ),
    ]
