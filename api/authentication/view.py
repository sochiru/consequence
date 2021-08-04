import urllib
from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import signing
from integrations.auth import AuthConnect
from data.models.user_cred import UserCred
from .serializers import UserCredSerializer


class AuthLinkView(APIView):
    """Get auth link view"""
    permission_classes = (IsAuthenticated,)

    def get(self, _):
        """Get auth link"""
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
        """Exchange for token"""

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

        auth_connect = AuthConnect(token=None)
        res = auth_connect.exchange_token(data=data)

        if res.status_code == 200:
            data = res.json()

            obj, _ = UserCred.objects.update_or_create(
                client_id=client_id,
                defaults={
                    'client_id': client_id,
                    'access_token': signing.dumps(data['access_token']),
                    'expires_in': data['expires_in'],
                    'token_type': data['token_type'],
                    'refresh_token': signing.dumps(data['refresh_token']),
                    'scope': data['scope']
                })

            serializer = UserCredSerializer(obj)
            return Response(serializer.data)

        return Response(res.json(), status=res.status_code)


class UserLogoutView(APIView):
    """User logout view"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()

        return Response()
