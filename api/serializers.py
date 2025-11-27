from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import UserProfile, User

class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer for JWT token creation with verification check
    """
    account = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        account = attrs.get('account')
        password = attrs.get('password')

        # Check if account is email or username
        if '@' in account:
            try:
                user_obj = User.objects.get(email=account)
                username = user_obj.username
            except User.DoesNotExist:
                # If email not found, we still pass the email as username to authenticate
                # so it fails with the standard error
                username = account
        else:
            username = account

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



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_verified', 'profile']