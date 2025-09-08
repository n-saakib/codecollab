from datetime import timedelta

from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_active = models.DateTimeField("Last Active", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)

    def is_online(self) -> bool:
        """
            Returns True if the user was active in the last 5 minutes.
        """
        if not self.last_active:
            return False
        now = timezone.now()
        return now < self.last_active + timedelta(minutes=5)