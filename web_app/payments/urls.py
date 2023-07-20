from django.urls import path
from .views import payment_confirm, addDonate, create_payout_method
from .api import PayoutApiView, SetDefaultPayoutMethodApi

urlpatterns = [
    path('donate/<str:username>', addDonate, name='create_payment'),
    path('payment/confirm/', payment_confirm, name='payment_confirm'),
    path('payout/', PayoutApiView.as_view(), name='payout'),
    path('payout_method/', SetDefaultPayoutMethodApi, name='payout_method'),
    path('payout_streamer/', create_payout_method, name='create_payout'),
]