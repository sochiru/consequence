from django.db import models
from .card import Card


class CardBalance(models.Model):
    currency = models.CharField(max_length=128)
    available = models.FloatField()
    current = models.FloatField()
    credit_limit = models.FloatField()
    last_statement_date = models.DateTimeField()
    last_statement_balance = models.FloatField()
    payment_due = models.FloatField()
    payment_due_date = models.DateTimeField()
    update_timestamp = models.DateTimeField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.current
