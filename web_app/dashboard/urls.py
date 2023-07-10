from django.urls import path
import dashboard.views as views
import dashboard.api as API

urlpatterns = [
    path('profile/', views.ProfileStreamerView.as_view(), name='profile'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('donations/', views.AllDonationsView.as_view(), name='donations'),
    path('withdraw/', views.WithdrawView.as_view(), name='withdraw'),
    path('change_profile/', views.change_profile, name='change_profile'),
    path('change_settings/', views.change_settings, name='change_settings'),
    path('payout_streamer/', views.create_payout_method, name='create_payout'),
    path('api/v1/streamers/', API.AccountsDonationsApiView.as_view()),
    path('api/v1/donates/', API.DonatesInfoApiView.as_view()),
    path('api/v1/streamer/', API.AccountDonationsApiView.as_view()),
    path('api/v1/donates_streamer/', API.DonatesRelatedStreamerInfoApiView.as_view()),
    path('api/v1/donates_for_week/', API.DonatesForWeekApiView.as_view()),
]