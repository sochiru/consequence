from ..serializers.user import UserSerializer
from rest_framework.generics import CreateAPIView
from ..serializers.user import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


class UserRegisterView(CreateAPIView):
    """
    Creates the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
