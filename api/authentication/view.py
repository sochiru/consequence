from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from integrations.auth import AuthConnect
import urllib

from django.conf import settings


class AuthView(APIView):
    """Card list view"""
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request):
        """Get cards list"""
        host_auth = settings.INTEGRATIONS['TRUELAYER']['HOST_AUTH']
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        redirect_uri = settings.INTEGRATIONS['TRUELAYER']['REDIRECT_URI']

        query_params = {
            'response_type': 'code',
            'client_id': client_id,
            'scope': 'info accounts balance cards transactions offline_access',
            'providers': 'uk-ob-all uk-oauth-all uk-cs-mock',
            'response_mode': 'form_post'
        }
        query = urllib.parse.urlencode(query_params, doseq=True).replace('+', '%20')
        auth_uri = f'{host_auth}?{query}&redirect_uri={redirect_uri}'

        return HttpResponse(auth_uri)


class AuthCallbackView(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        """Get cards list"""

        code = request.data['code']
        client_id = settings.INTEGRATIONS['TRUELAYER']['CLIENT_ID']
        secret = settings.INTEGRATIONS['TRUELAYER']['SECRET']
        redirect_uri = settings.INTEGRATIONS['TRUELAYER']['REDIRECT_URI']

        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': secret,
            'redirect_uri': redirect_uri,
            'code': code
        }

        payload = urllib.parse.urlencode(data, doseq=True).replace('+', '%20')

        auth_connect = AuthConnect(token=None)
        res = auth_connect.exchange_token(data=payload)

        return Response(res.json(), status=res.status_code)
