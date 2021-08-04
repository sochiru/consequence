from data.models.account_transaction import AccountTransaction, AccountTransactionPending
from rest_framework.response import Response
from integrations.accounts import AccountsConnect
from data.models.account import Account
from django.shortcuts import get_object_or_404
from data.models.user_cred import UserCred
from .serializer import AccountSerializer, AccountTransactionPendingSerializer, AccountTransactionSerializer
from rest_framework import viewsets
from django.conf import settings
from django.core import signing
from .helpers import sync_account_transactions, sync_accounts


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        user_cred = UserCred.objects.filter(client_id=client_id).first()
        if user_cred:
            access_token = signing.loads(user_cred.access_token)
            account_connect = AccountsConnect(token=access_token)
            response = account_connect.get()

            accounts_list = response.json()['results']
            sync_accounts(accounts_list)
        return super().list(request, *args, **kwargs)


class AccountDetailViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def retrieve(self, request, account_id=None):
        obj = get_object_or_404(Account, account_id=account_id)
        serialized = AccountSerializer(obj)
        return Response(serialized.data)


class AccountTransactionsViewSet(viewsets.ModelViewSet):
    queryset = AccountTransaction.objects.all()
    serializer_class = AccountTransactionSerializer

    def transactions(self, request, account_id=None):
        account_obj = get_object_or_404(Account, account_id=account_id)
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        user_cred = UserCred.objects.filter(client_id=client_id).first()

        if user_cred:
            access_token = signing.loads(user_cred.access_token)
            account_connect = AccountsConnect(token=access_token)
            response = account_connect.get_account_transactions(account_id)

            transasctions = response.json()['results']
            print(transasctions)
            sync_account_transactions(AccountTransaction, transasctions, account_obj)

        account_transactions = AccountTransaction.objects.filter(account=account_obj)
        serialized = AccountTransactionSerializer(account_transactions, many=True)
        return Response(serialized.data)


class AccountTransactionsPendingViewSet(viewsets.ModelViewSet):
    queryset = AccountTransactionPending.objects.all()
    serializer_class = AccountTransactionPendingSerializer

    def transactions_pending(self, request, account_id=None):
        account_obj = get_object_or_404(Account, account_id=account_id)
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        user_cred = UserCred.objects.filter(client_id=client_id).first()

        if user_cred:
            access_token = signing.loads(user_cred.access_token)
            card_connect = AccountsConnect(token=access_token)
            response = card_connect.get_account_transactions_pending(account_id)

            transasctions_pending = response.json()['results']
            sync_account_transactions(AccountTransactionPending, transasctions_pending, account_obj)

        card_transactions = AccountTransactionPending.objects.filter(account=account_obj)

        serialized = AccountTransactionPendingSerializer(card_transactions, many=True)
        return Response(serialized.data)
