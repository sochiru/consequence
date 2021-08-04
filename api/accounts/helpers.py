from data.models.account import Account


def sync_accounts(accounts_list):
    for account in accounts_list:
        Account.objects.update_or_create(
            account_id=account['account_id'],
            defaults={
                'account_type': account['account_type'],
                'account_number': account['account_number'],
                'currency': account['currency'],
                'display_name': account['display_name'],
                'update_timestamp': account['update_timestamp'],
                'provider': account['provider']
            }
        )


def sync_account_transactions(model, transaction_list, account):
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
                'account': account
            }
        )
