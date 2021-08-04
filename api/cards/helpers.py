from data.models.card_transaction import CardRunningBalance, CardTransaction, CardTransactionMeta, CardTransactionPending
from data.models.card import Card, CardProvider


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
