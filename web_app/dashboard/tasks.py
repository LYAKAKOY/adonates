from typing import List, Dict
from celery import shared_task
from django.db.models import Sum
from users.models import DonateModel
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from django.utils.translation import gettext as _


@shared_task(serializer='json')
def top_donations(username: str) -> List[Dict]:
    donations = DonateModel.objects.select_related('payment', 'streamer__user').values('nickname').filter(
        streamer__user__username=username, payment__status='succeeded').annotate(
        total_donated_sum=Sum('payment__payment_sum')).order_by('-total_donated_sum')
    return list(donations)


@shared_task
def statistics_for_last_six_months(username: str) -> List[Dict]:
    current_time = datetime.now()
    donates_for_last_six_months = []
    for month in range(int((current_time - relativedelta(months=5)).month),
                       int((current_time + relativedelta(months=1)).month)):
        month_sum = DonateModel.objects.filter(
            streamer__user__username=username, payment__status='succeeded',
            payment__payment_date__month=month).aggregate(sum=Sum('payment__payment_sum'))['sum'] or 0
        donates_for_last_six_months.append({
            'month': _(calendar.month_name[month]),
            'month_sum': month_sum,
        })
    return donates_for_last_six_months
