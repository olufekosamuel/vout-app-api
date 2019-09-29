from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, status, viewsets
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    password = serializers.CharField(min_length=8,write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("Those passwords don't match.")
        return attrs
        
    def create(self, validated_data):
        del validated_data["password2"]
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'],
                validated_data['password'])
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2')

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)