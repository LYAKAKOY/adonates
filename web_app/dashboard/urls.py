from django.urls import path
from .views import StatisticsView, WithdrawView

urlpatterns = [
    path('dashboard/', StatisticsView.as_view(), name='dashboard'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
]