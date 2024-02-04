from django.conf import settings
from django.db import models


# This model will include the user for stuff like username, email, password
# In addition it will build on top with more 'profile' oriented stuff. e.g: profile picture? bio?
# This model may just be removed later and 'profile' might just become more akin to 'account-settings'
# Depending on the project scope management and feature completion rate as this is not core functionality
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
