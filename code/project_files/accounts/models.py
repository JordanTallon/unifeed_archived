from django.contrib.auth.models import AbstractUser
from django.db import models
from articles.models import RecentlyRead


class User(AbstractUser):
    email = models.EmailField(unique=True)
    track_history = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # store the original track history value when the account is made
        self.__original_track_history = self.track_history

    def save(self, *args, **kwargs):
        # If track_history was True and now its being set to False
        if self.__original_track_history and not self.track_history:
            # Delete all reading history
            RecentlyRead.objects.filter(user=self).delete()

        super(User, self).save(*args, **kwargs)

        # set the original track history to the new one
        self.__original_track_history = self.track_history
