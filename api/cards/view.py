from api.cards.serializer import CardSerializer
from rest_framework import viewsets
from requests.models import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from integrations.cards import CardsConnect
from data.models.card import Card


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


class CardsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        obj = Card.objects.filter(account_id=pk).first()
        if obj:
            serialized = CardSerializer(obj)
            return Response(serialized.data)
        return Response({'detail': 'Not Found.'})
