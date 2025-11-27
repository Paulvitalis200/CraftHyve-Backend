from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer for JWT token creation with verification check
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                {'detail': 'Unable to log in with provided credentials.'}
            )

        # Check if user is verified
        if not user.is_verified:
            raise serializers.ValidationError(
                {'detail': 'Please verify your account before logging in.'}
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }