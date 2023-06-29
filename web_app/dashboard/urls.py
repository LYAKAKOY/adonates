from django.urls import path
from .views import StatisticsView, WithdrawView
import dashboard.api as API

urlpatterns = [
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('api/v1/streamers/', API.AccountsDonationsApiView.as_view()),
    path('api/v1/donates/', API.DonatesInfoApiView.as_view()),
    path('api/v1/streamer/', API.AccountDonationsApiView.as_view()),
    path('api/v1/donates_streamer/', API.DonatesRelatedStreamerInfoApiView.as_view()),
    path('api/v1/donates_for_week/', API.DonatesForWeekApiView.as_view()),
]