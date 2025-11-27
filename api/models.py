from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    
    def generate_verification_token(self):
        """Generate a new verification token"""
        self.verification_token = uuid.uuid4()
        self.save()
        return self.verification_token