import requests
from yookassa import Configuration, Payout
from yookassa.domain.common import PaymentMethodType
from yookassa.domain.models.currency import Currency


class YouKassaPayout:
    __slots__ = ['agent_id', 'secret_key']

    def __init__(self, agent_id: Configuration.account_id, secret_key: Configuration.secret_key):
        self.agent_id = agent_id
        self.secret_key = secret_key

    def create_payout_yookassa(self, sum_of_money: int, account_number: int) -> Payout.create:
        Configuration.account_id = self.agent_id
        Configuration.secret_key = self.secret_key
        query = {
            "amount": {
                "value": sum_of_money,
                "currency": Currency.RUB
            },
            "payout_destination_data": {
                'type': PaymentMethodType.YOO_MONEY,
                'account_number': account_number
            },
            "description": "Вывод средств"
        }
        return Payout.create(query)

    def create_payout_bank_card(self, sum_of_money: int, card_number: int) -> Payout.create:
        Configuration.account_id = self.agent_id
        Configuration.secret_key = self.secret_key
        query = {
            "amount": {
                "value": sum_of_money,
                "currency": Currency.RUB
            },
            "payout_destination_data": {
                'type': PaymentMethodType.BANK_CARD,
                'card': {
                    'number': card_number
                }
            },
            "description": "Вывод средств"
        }
        return Payout.create(query)

    def create_payout_sbp(self, sum_of_money: int, bank_id: int, phone: int) -> Payout.create:
        Configuration.account_id = self.agent_id
        Configuration.secret_key = self.secret_key
        query = {
            "amount": {
                "value": sum_of_money,
                "currency": Currency.RUB
            },
            "payout_destination_data": {
                'type': PaymentMethodType.SBP,
                'bank_id': bank_id,
                'phone': phone
            },
            "description": "Вывод средств"
        }
        return Payout.create(query)

    def get_bank_id(self) -> dict:
        url = 'https://api.yookassa.ru/v3/sbp_banks'
        auth = (self.agent_id, self.secret_key)

        response = requests.get(url, auth=auth)

        return response.json()
