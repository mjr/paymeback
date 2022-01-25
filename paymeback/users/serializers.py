from rest_framework import serializers

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
