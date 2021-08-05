from data.models.account_transaction import AccountTransaction, AccountTransactionPending
from data.models.account import Account
from django.conf import settings
from django.core import signing
from integrations.accounts import AccountsConnect
from data.models.user_cred import UserCred


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


def get_accounts():
    client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
    user_cred = UserCred.objects.filter(client_id=client_id).first()
    if user_cred:
        access_token = signing.loads(user_cred.access_token)
        account_connect = AccountsConnect(token=access_token)
        response = account_connect.get()
        if response.status_code == 200:
            accounts_list = response.json()['results']
            sync_accounts(accounts_list)


def get_account_transactions(account_id, account_obj):
    client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
    user_cred = UserCred.objects.filter(client_id=client_id).first()

    if user_cred:
        access_token = signing.loads(user_cred.access_token)
        account_connect = AccountsConnect(token=access_token)
        response = account_connect.get_account_transactions(account_id)

        transasctions = response.json()['results']
        sync_account_transactions(AccountTransaction, transasctions, account_obj)


def get_account_transactions_pending(account_id, account_obj):

    client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
    user_cred = UserCred.objects.filter(client_id=client_id).first()

    if user_cred:
        access_token = signing.loads(user_cred.access_token)
        account_connect = AccountsConnect(token=access_token)
        response = account_connect.get_account_transactions_pending(account_id)

        transasctions_pending = response.json()['results']
        sync_account_transactions(AccountTransactionPending, transasctions_pending, account_obj)
