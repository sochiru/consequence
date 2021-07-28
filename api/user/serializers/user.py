from copy import error
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=255, min_length=4, required=True)
    password = serializers.CharField(min_length=8, max_length=65, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id',  'email', 'username', 'password']

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']):
            raise serializers.ValidationError({'email', ('Email exists')})
        return super().validate(attrs)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
