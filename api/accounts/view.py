from requests.models import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from integrations.accounts import AccountsConnect


class AccountsListView(APIView):
    """account list view"""

    def get(self, request):
        """Get Accounts list"""
        account_connect = AccountsConnect(token='')
        response = account_connect.get()
        return Response(response.json())


class AccountsDetailView(APIView):
    """Account detail view"""

    def get(self, request, account_id):
        """Get Accounts detail"""
        account_connect = AccountsConnect(token='')
        response = account_connect.get(account_id)
        return Response(response.json())


class AccountsDetailBalanceView(APIView):
    """Account detail balance view"""

    def get(self, request, account_id):
        """Get Accounts detail balance"""
        account_connect = AccountsConnect(token='')
        response = account_connect.get_account_balance(account_id)
        return Response(response.json())


class AccountsDetailTransactionsView(APIView):
    """Account detail transactions view"""

    def get(self, request, account_id):
        """Get Accounts detail transactions"""
        account_connect = AccountsConnect(token='')
        response = account_connect.get_account_transactions(account_id)
        return Response(response.json())


class AccountsDetailTransactionsPendingView(APIView):
    """Account detail transactions view"""

    def get(self, request, account_id):
        """Get Accounts detail transactions"""
        account_connect = AccountsConnect(token='')
        response = account_connect.get_account_transactions_pending(account_id)
        return Response(response.json())
