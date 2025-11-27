from django.urls import path
from api.views import SendVerificationEmailView, VerifyEmailView

urlpatterns = [
    path('send-verification-email/', SendVerificationEmailView.as_view(), name='send_verification_email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
]