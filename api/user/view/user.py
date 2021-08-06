from data.models.user_cred import UserCred
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.user import ChangePasswordSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from ..serializers.user import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core import signing


class UserRegisterView(CreateAPIView):
    """
    Creates the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserInfoViewSet(APIView):
    permission_classes = []  # disables permission

    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)

        user_cred = UserCred.objects.get(user=user)

        user_info = {
            'email': user.email,
            'username': user.username,
            'authorized': True if user_cred.access_token else False
        }

        return Response(user_info)

    def put(self, request):
        user = get_user_model().objects.get(username=request.user.username)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserChangePasswordView(UpdateAPIView):
    """User change password view"""
    permission_classes = []  # disables permission

    def update(self, request):
        """Update user password"""
        serializer = ChangePasswordSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(request.data['new_password'])
        self.request.user.save()

        return Response({'detail': 'success'})
