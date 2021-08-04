from django.db import models
from django.contrib.auth import get_user_model


class UserCred(models.Model):
    """User creds"""
    client_id = models.TextField(null=True)
    access_token = models.TextField(null=True)
    expires_in = models.IntegerField(null=True)
    token_type = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    scope = models.TextField(null=True)
