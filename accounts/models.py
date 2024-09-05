from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    verification_attempts = models.IntegerField(default=0)  # Track the number of attempts
    code_created_at = models.DateTimeField(null=True, blank=True)  # Track when the code was generated

    # Constants for code validity
    CODE_VALIDITY_PERIOD = 10  # Code validity in minutes

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.verification_attempts = 0  # Reset attempts when generating a new code
        self.code_created_at = timezone.now()  # Set the time when code was generated
        self.save()

    def is_code_valid(self):
        if not self.code_created_at:
            return False
        return (timezone.now() - self.code_created_at).total_seconds() <= self.CODE_VALIDITY_PERIOD * 60

