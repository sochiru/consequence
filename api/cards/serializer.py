from data.models.card_transaction import CardTransaction, CardTransactionPending
from rest_framework.serializers import ModelSerializer
from data.models.card import Card, CardProvider


class CardProviderSerializer(ModelSerializer):
    class Meta:
        model = CardProvider
        fields = ('provider_id', 'display_name', 'logo_uri')


class CardSerializer(ModelSerializer):
    provider = CardProviderSerializer(read_only=True)

    class Meta:
        model = Card
        fields = '__all__'


class CardTransactionSerializer(ModelSerializer):

    class Meta:
        model = CardTransaction
        fields = '__all__'


class CardTransactionPendingSerializer(ModelSerializer):

    class Meta:
        model = CardTransactionPending
        fields = '__all__'
