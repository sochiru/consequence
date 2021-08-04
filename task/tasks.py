# pylint:disable=import-outside-toplevel
from __future__ import absolute_import
from data.models.card import Card
from data.models.account import Account

from celery import shared_task
from api.accounts.helpers import get_accounts, get_account_transactions, get_account_transactions_pending
from api.cards.helpers import get_cards, get_card_transactions, get_card_transactions_pending


@shared_task
def accounts():
    get_accounts()
    accounts = Account.objects.all()
    for account in accounts:
        get_account_transactions(account.account_id, account)
        get_account_transactions_pending(account.account_id, account)


@shared_task
def cards():
    get_cards()
    cards = Card.objects.all()
    for card in cards:
        get_card_transactions(card.account_id, card)
        get_card_transactions_pending(card.account_id, card)
