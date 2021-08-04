from django.db import models


class Account(models.Model):
    account_id = models.CharField(max_length=128)
    account_type = models.CharField(max_length=128)
    account_number = models.JSONField(max_length=128)
    currency = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    update_timestamp = models.DateTimeField()
    provider = models.CharField(max_length=128)
    update_timestamp = models.DateTimeField()
    provider = models.JSONField(max_length=128)

    def __str__(self):
        return self.display_name
