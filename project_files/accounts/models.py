from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    track_history = models.BooleanField(default=False)

    def toggle_track_history(self):
        self.track_history = not self.track_history
