from django.db import models
from .account import Account


class AccountTransaction(models.Model):
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=128)
    transaction_type = models.CharField(max_length=128)
    transaction_category = models.CharField(max_length=128)
    transaction_classification = models.JSONField()
    amount = models.FloatField()
    currency = models.CharField(max_length=128)
    transaction_id = models.CharField(max_length=128)
    provider_transaction_id = models.CharField(max_length=128, null=True)
    normalised_provider_transaction_id = models.CharField(max_length=128, null=True)
    running_balance = models.JSONField(null=True)
    merchant_name = models.CharField(max_length=128, null=True)
    meta = models.JSONField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_id


class AccountTransactionPending(models.Model):
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=128)
    transaction_type = models.CharField(max_length=128)
    transaction_category = models.CharField(max_length=128)
    transaction_classification = models.JSONField()
    amount = models.FloatField()
    currency = models.CharField(max_length=128)
    transaction_id = models.CharField(max_length=128)
    provider_transaction_id = models.CharField(max_length=128, null=True)
    normalised_provider_transaction_id = models.CharField(max_length=128, null=True)
    running_balance = models.JSONField(null=True)
    merchant_name = models.CharField(max_length=128, null=True)
    meta = models.JSONField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_id
