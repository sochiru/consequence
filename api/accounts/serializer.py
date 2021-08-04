from data.models.account_transaction import AccountTransaction, AccountTransactionPending
from data.models.account import Account
from rest_framework.serializers import ModelSerializer


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class AccountTransactionSerializer(ModelSerializer):

    class Meta:
        model = AccountTransaction
        fields = '__all__'


class AccountTransactionPendingSerializer(ModelSerializer):

    class Meta:
        model = AccountTransactionPending
        fields = '__all__'
