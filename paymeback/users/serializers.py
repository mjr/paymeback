from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    expires_in = serializers.SerializerMethodField()
    token_type = serializers.SerializerMethodField()
    scope = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'nickname',
            'full_name',
            'token',
            'expires_in',
            'token_type',
            'scope',
            'refresh_token',
        )

    def get_token(self, obj):
        return self.context['access_token']

    def get_expires_in(self, obj):
        return self.context['expires_in']

    def get_token_type(self, obj):
        return self.context['token_type']

    def get_scope(self, obj):
        return self.context['scope']

    def get_refresh_token(self, obj):
        return self.context['refresh_token']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
