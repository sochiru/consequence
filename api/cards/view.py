from data.models.card_transaction import CardTransaction, CardTransactionPending
from django.shortcuts import get_object_or_404
from data.models.user_cred import UserCred
from api.cards.serializer import CardSerializer, CardTransactionPendingSerializer, CardTransactionSerializer
from rest_framework import viewsets
from requests.models import Response
from rest_framework.response import Response
from integrations.cards import CardsConnect
from data.models.card import Card
from django.conf import settings
from django.core import signing
from .helpers import sync_card_transactions,  sync_cards


class CardsViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def list(self, request, *args, **kwargs):
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        user_cred = UserCred.objects.filter(client_id=client_id).first()
        if user_cred:
            access_token = signing.loads(user_cred.access_token)
            card_connect = CardsConnect(token=access_token)
            response = card_connect.get()

            cards_list = response.json()['results']
            sync_cards(cards_list)
        return super().list(request, *args, **kwargs)


class CardDetailViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def retrieve(self, request, card_id=None):
        obj = get_object_or_404(Card, account_id=card_id)
        serialized = CardSerializer(obj)
        return Response(serialized.data)


class CardsTransactionsViewSet(viewsets.ModelViewSet):
    queryset = CardTransaction.objects.all()
    serializer_class = CardTransactionSerializer

    def transactions(self, request, card_id=None):
        card_obj = get_object_or_404(Card, account_id=card_id)
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        user_cred = UserCred.objects.filter(client_id=client_id).first()

        if user_cred:
            access_token = signing.loads(user_cred.access_token)
            card_connect = CardsConnect(token=access_token)
            response = card_connect.get_card_transactions(card_id)

            transasctions = response.json()['results']
            sync_card_transactions(CardTransaction, transasctions, card_obj)

        card_transactions = CardTransaction.objects.filter(card=card_obj)

        serialized = CardTransactionSerializer(card_transactions, many=True)
        return Response(serialized.data)


class CardsTransactionsPendingViewSet(viewsets.ModelViewSet):
    queryset = CardTransaction.objects.all()
    serializer_class = CardTransactionSerializer

    def transactions_pending(self, request, card_id=None):
        card_obj = get_object_or_404(Card, account_id=card_id)
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        user_cred = UserCred.objects.filter(client_id=client_id).first()

        if user_cred:
            access_token = signing.loads(user_cred.access_token)
            card_connect = CardsConnect(token=access_token)
            response = card_connect.get_card_transactions_pending(card_id)

            transasctions_pending = response.json()['results']
            sync_card_transactions(CardTransactionPending, transasctions_pending, card_obj)

        card_transactions = CardTransactionPending.objects.filter(card=card_obj)

        serialized = CardTransactionPendingSerializer(card_transactions, many=True)
        return Response(serialized.data)
