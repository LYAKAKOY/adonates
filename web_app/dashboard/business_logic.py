from celery.result import AsyncResult
from django.db.models import Sum
from django.http import HttpRequest
from users.models import DonateModel
from .tasks import statistics_for_last_five_months


def dashboard_logic(request: HttpRequest) -> dict:
    result = {}
    statistics_by_months = statistics_for_last_five_months.delay(request.user.username)
    result_task = AsyncResult(statistics_by_months.task_id)
    donations = DonateModel.objects.filter(
        streamer__user__username=request.user.username, payment__status='succeeded').order_by(
        '-payment__payment_date').only('nickname', 'message').annotate(
        donate_sum=Sum('payment__payment_sum'))
    result['donations'] = donations[:10]
    result['statistics_by_months'] = result_task.get()
    return result
