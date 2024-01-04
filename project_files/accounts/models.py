from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    track_analytics = models.BooleanField(default=False)

    def toggle_analytics(self):
        self.track_analytics = not self.track_analytics
