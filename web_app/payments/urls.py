from django.urls import path
from .views import payment_confirm, addDonate, payout_notification

urlpatterns = [
    path('donate/<str:username>', addDonate, name='create_payment'),
    path('payment/confirm/', payment_confirm, name='payment_confirm'),
    path('payount/notification/', payout_notification, name='payout_notification'),
]