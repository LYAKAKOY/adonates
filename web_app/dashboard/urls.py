from django.urls import path
from .views import StatisticsView, WithdrawView, AllDonationsView, ProfileStreamerView, create_payout_method
import dashboard.api as API

urlpatterns = [
    path('profile/', ProfileStreamerView.as_view(), name='profile'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('donations/', AllDonationsView.as_view(), name='donations'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('payout_streamer/', create_payout_method, name='create_payout'),
    path('api/v1/streamers/', API.AccountsDonationsApiView.as_view()),
    path('api/v1/donates/', API.DonatesInfoApiView.as_view()),
    path('api/v1/streamer/', API.AccountDonationsApiView.as_view()),
    path('api/v1/donates_streamer/', API.DonatesRelatedStreamerInfoApiView.as_view()),
    path('api/v1/donates_for_week/', API.DonatesForWeekApiView.as_view()),
]