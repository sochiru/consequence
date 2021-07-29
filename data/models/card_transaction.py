from django.db import models
from .card import Card


class CardRunningBalance(models.Model):
    currency = models.CharField(max_length=128)
    amount = models.FloatField()


class CardTransactionMeta(models.Model):
    provider_transaction_category = models.CharField(max_length=128)


class CardTransaction(models.Model):
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=128)
    transaction_type = models.CharField(max_length=128)
    transaction_category = models.CharField(max_length=128)
    transaction_classification = models.JSONField()
    amount = models.FloatField()
    currency = models.CharField(max_length=128)
    transaction_id = models.CharField(max_length=128)
    provider_transaction_id = models.CharField(max_length=128)
    normalised_provider_transaction_id = models.CharField(max_length=128)
    running_balance = models.ForeignKey(CardRunningBalance, on_delete=models.CASCADE)
    merchant_name = models.CharField(max_length=128)
    meta = models.JSONField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_id
