from rest_framework.serializers import ModelSerializer
from data.models.card import Card


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('account_id', 'card_network', 'card_type', 'currency', 'display_name',
                  'partial_card_number', 'name_on_card', 'update_timestamp', 'provider')
