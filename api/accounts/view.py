from rest_framework.views import APIView
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
from .helpers import get_accounts, get_account_transactions, get_account_transactions_pending


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        get_accounts()
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

    def list(self, request, account_id=None):
        account_obj = get_object_or_404(Account, account_id=account_id)
        get_account_transactions(account_id, account_obj)

        account_transactions = AccountTransaction.objects.filter(account=account_obj)
        serialized = AccountTransactionSerializer(account_transactions, many=True)
        return Response(serialized.data)


class AccountTransactionsPendingViewSet(viewsets.ModelViewSet):
    queryset = AccountTransactionPending.objects.all()
    serializer_class = AccountTransactionPendingSerializer

    def list(self, request, account_id=None):
        account_obj = get_object_or_404(Account, account_id=account_id)
        get_account_transactions_pending(account_id, account_obj)
        account_transactions_pending = AccountTransactionPending.objects.filter(account=account_obj)

        serialized = AccountTransactionPendingSerializer(account_transactions_pending, many=True)
        return Response(serialized.data)


class AccountsWebhook(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        """Exchange for token"""

        data = request.data
        print(data)

        return Response()
