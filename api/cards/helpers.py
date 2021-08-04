from data.models.card_transaction import CardTransaction, CardTransactionPending
from integrations.cards import CardsConnect
from data.models.card import Card, CardProvider
from django.conf import settings
from django.core import signing
from integrations.accounts import AccountsConnect
from data.models.user_cred import UserCred


def sync_cards(cards_list):
    for card in cards_list:
        card_provider, _ = CardProvider.objects.update_or_create(
            provider_id=card['provider']['provider_id'], defaults={
                'display_name': card['provider']['display_name'],
                'logo_uri': card['provider']['logo_uri'],
            })

        Card.objects.update_or_create(
            account_id=card['account_id'],
            defaults={
                'card_network': card['card_network'],
                'card_type': card['card_type'],
                'currency': card['currency'],
                'display_name': card['display_name'],
                'partial_card_number': card['partial_card_number'],
                'name_on_card': card['name_on_card'],
                'update_timestamp': card['update_timestamp'],
                'provider': card_provider
            }
        )


def sync_card_transactions(model, transaction_list, card):
    for transaction in transaction_list:
        model.objects.update_or_create(
            transaction_id=transaction['transaction_id'],
            defaults={
                'timestamp': transaction['timestamp'],
                'description': transaction['description'],
                'transaction_type': transaction['transaction_type'],
                'transaction_category': transaction['transaction_category'],
                'transaction_classification': transaction['transaction_classification'],
                'amount': transaction['amount'],
                'currency': transaction['currency'],
                'provider_transaction_id': transaction['provider_transaction_id'] if 'provider_transaction_id' in transaction else None,
                'normalised_provider_transaction_id': transaction['normalised_provider_transaction_id'] if 'normalised_provider_transaction_id' in transaction else None,
                'merchant_name': transaction['merchant_name'] if 'merchant_name' in transaction else None,
                'running_balance': transaction['running_balance'] if 'running_balance' in transaction else None,
                'meta': transaction['meta'],
                'card': card
            }
        )


def get_cards():
    client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
    user_cred = UserCred.objects.filter(client_id=client_id).first()
    if user_cred:
        access_token = signing.loads(user_cred.access_token)
        card_connect = CardsConnect(token=access_token)
        response = card_connect.get()

        cards_list = response.json()['results']
        sync_cards(cards_list)


def get_card_transactions(card_id, card_obj):
    client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
    user_cred = UserCred.objects.filter(client_id=client_id).first()

    if user_cred:
        access_token = signing.loads(user_cred.access_token)
        card_connect = CardsConnect(token=access_token)
        response = card_connect.get_card_transactions(card_id)

        transasctions = response.json()['results']
        sync_card_transactions(CardTransaction, transasctions, card_obj)


def get_card_transactions_pending(card_id, card_obj):
    client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
    user_cred = UserCred.objects.filter(client_id=client_id).first()

    if user_cred:
        access_token = signing.loads(user_cred.access_token)
        card_connect = CardsConnect(token=access_token)
        response = card_connect.get_card_transactions_pending(card_id)

        transasctions_pending = response.json()['results']
        sync_card_transactions(CardTransactionPending, transasctions_pending, card_obj)
