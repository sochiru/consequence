from copy import error
from data.models.user_cred import UserCred
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=255, min_length=4, required=True)
    password = serializers.CharField(min_length=8, max_length=65, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id',  'email', 'username', 'password')

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']):
            raise serializers.ValidationError({'email', ('Email exists')})
        if User.objects.filter(email=attrs['username']):
            raise serializers.ValidationError({'username', ('Username exists')})
        return super().validate(attrs)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        UserCred.objects.create(user=user)

        return user
