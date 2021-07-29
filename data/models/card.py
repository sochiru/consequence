from django.db import models


class CardProvider(models.Model):
    provider_id = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    logo_uri = models.CharField(max_length=128)

    def __str__(self):
        return self.display_name


class Card(models.Model):
    account_id = models.CharField(max_length=128)
    card_network = models.CharField(max_length=128)
    card_type = models.CharField(max_length=128)
    currency = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    partial_card_number = models.CharField(max_length=128)
    name_on_card = models.CharField(max_length=128)
    update_timestamp = models.DateTimeField()
    provider = models.ForeignKey(CardProvider, on_delete=models.CASCADE)

    def __str__(self):
        return self.display_name
