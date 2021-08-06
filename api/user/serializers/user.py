from copy import error
from data.models.user_cred import UserCred
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
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

    def update(self, instance, validated_data):
        print(instance)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Your old password was entered incorrectly. Please enter it again.')
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_confirm_password(self, value):
        if value != self.initial_data.get('confirm_password', None):
            raise serializers.ValidationError("Password mismatch.")
        return value
