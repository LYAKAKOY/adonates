from decimal import Decimal
from yookassa.domain.response import PaymentResponse
from yookassa import Configuration, Payment


class YouKassaPayment:
    __slots__ = ['account_id', 'secret_key']

    def __init__(self, account_id: Configuration.account_id, secret_key: Configuration.secret_key):
        self.account_id = account_id
        self.secret_key = secret_key

    def create_payment(self, donate_sum: Decimal, redirect_url: str):
        Configuration.account_id = self.account_id
        Configuration.secret_key = self.secret_key
        query = {
            "amount": {
                "value": f"{donate_sum}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": redirect_url
            },
            "capture": True,
            "description": "Оплата заказа"
        }
        payment = Payment.create(query)
        return payment

    def get_payment(self, payment_id: int) -> PaymentResponse:
        Configuration.account_id = self.account_id
        Configuration.secret_key = self.secret_key
        payment = Payment.find_one(payment_id=payment_id)
        return payment
