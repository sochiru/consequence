from rest_framework import serializers
from django.core import signing
from data.models.user_cred import UserCred


class UserCredSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCred
        fields = ('access_token', 'expires_in', 'token_type', 'refresh_token', 'scope')

    def to_representation(self, instance):
        return {
            'client_id': instance.client_id,
            'access_token': signing.loads(instance.access_token),
            'expires_in': instance.expires_in,
            'token_type': instance.token_type,
            'refresh_token': signing.loads(instance.refresh_token),
            'scope': instance.scope
        }
