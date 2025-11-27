from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import CustomTokenObtainPairSerializer
from api.models import User
from django.core.mail import send_mail
from django.conf import settings


class CustomTokenObtainPairView(APIView):
    """
    Custom view for obtaining JWT tokens that checks user verification
    """
    permission_classes = []

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SendVerificationEmailView(APIView):
    """
    Send verification email to user
    """
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User with this email does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user.is_verified:
            return Response(
                {'message': 'User is already verified'}, 
                status=status.HTTP_200_OK
            )
        
        # Generate verification token
        token = user.generate_verification_token()
        
        # Create verification link
        verification_link = f"{request.scheme}://{request.get_host()}/api/verify-email/?token={token}"
        
        # Send email (you'll need to configure email backend in settings.py)
        try:
            send_mail(
                subject='Verify your CraftHyve account',
                message=f'Please click the link to verify your account: {verification_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(
                {'message': 'Verification email sent successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyEmailView(APIView):
    """
    Verify user email with token
    """
    permission_classes = []

    def get(self, request):
        token = request.query_params.get('token')
        
        if not token:
            return Response(
                {'error': 'Token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(verification_token=token)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid verification token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user.is_verified:
            return Response(
                {'message': 'User is already verified'}, 
                status=status.HTTP_200_OK
            )
        
        # Verify the user
        user.is_verified = True
        user.verification_token = None  # Clear the token after verification
        user.save()
        
        return Response(
            {'message': 'Email verified successfully! You can now log in.'}, 
            status=status.HTTP_200_OK
        )
