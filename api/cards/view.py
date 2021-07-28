from requests.models import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from integrations.cards import CardsConnect


class CardsListView(APIView):
    """Card list view"""

    def get(self, request):
        """Get cards list"""
        card_connect = CardsConnect(token='')
        response = card_connect.get()
        return Response(response.json())


class CardsDetailView(APIView):
    """Card detail view"""

    def get(self, request, card_id):
        """Get cards detail"""
        card_connect = CardsConnect(token='')
        response = card_connect.get(card_id)
        return Response(response.json())


class CardsDetailBalanceView(APIView):
    """Card detail balance view"""

    def get(self, request, card_id):
        """Get cards detail balance"""
        card_connect = CardsConnect(token='')
        response = card_connect.get_card_balance(card_id)
        return Response(response.json())


class CardsDetailTransactionsView(APIView):
    """Card detail transactions view"""

    def get(self, request, card_id):
        """Get cards detail transactions"""
        card_connect = CardsConnect(token='')
        response = card_connect.get_card_transactions(card_id)
        return Response(response.json())


class CardsDetailTransactionsPendingView(APIView):
    """Card detail transactions view"""

    def get(self, request, card_id):
        """Get cards detail transactions"""
        card_connect = CardsConnect(token='')
        response = card_connect.get_card_transactions_pending(card_id)
        return Response(response.json())
