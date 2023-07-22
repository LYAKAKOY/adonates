from datetime import datetime
from typing import List, Dict
from celery.result import AsyncResult
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.http import HttpRequest
from social_django.models import UserSocialAuth
from payments.models import PayoutModel
from users.forms import ChangeProfileForm, ChangeGoalForm, ChangeSettingsForm
from users.models import DonateModel, StreamerCard, StreamerModel
from .tasks import statistics_for_last_six_months, top_donations
from payments.forms import PayoutAddForm


def statistics_logic(request: HttpRequest) -> dict:
    result = {}
    statistics_by_months = statistics_for_last_six_months.delay(request.user.username)
    result_task = AsyncResult(statistics_by_months.task_id)
    donations = DonateModel.objects.filter(
        streamer__user__username=request.user.username, payment__status='succeeded').order_by(
        '-payment__payment_date').only('nickname', 'message').annotate(
        donate_sum=Sum('payment__payment_sum'))
    result['donations'] = donations[:10]
    result['statistics_by_months'] = result_task.get()
    return result


def withdraw_logic(request: HttpRequest) -> dict:
    result = {}
    task = top_donations.delay(request.user.username)
    result_task = AsyncResult(task.task_id)
    result['withdrawals'] = PayoutModel.objects.filter(streamer=request.user).filter(
        status='succeeded').order_by('-payout_date')[:4]
    result['top_donations'] = result_task.get()
    cards = StreamerCard.objects.filter(streamer__user=request.user)
    result['type_cards'] = [card.type_payout for card in cards]
    result['form'] = PayoutAddForm()
    return result


def get_statistics_for_last_week(username: str) -> List[Dict]:
    current_time = datetime.now()
    statistics_for_last_week = []
    for day in range(int((current_time - relativedelta(days=6)).day), int((current_time + relativedelta(days=1)).day)):
        day_sum = DonateModel.objects.filter(
            streamer__user__username=username, payment__status='succeeded',
            payment__payment_date__year=current_time.year,
            payment__payment_date__month=current_time.month,
            payment__payment_date__day=day).aggregate(
            sum=Sum('payment__payment_sum'))['sum'] or 0
        statistics_for_last_week.append({
            'day': day,
            'month': current_time.month,
            'day_sum': day_sum
        })
    return list(statistics_for_last_week)
