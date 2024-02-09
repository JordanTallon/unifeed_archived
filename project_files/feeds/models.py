from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.apps import apps

# A feed folder allows for users to 'group' their feeds into different folders
# This is to allow the user to 1. organize their feeds, improving the user experience
# and 2. the user can click into their folder to see an aggregate feed containing all feeds in the folder


class FeedFolder(models.Model):
    name = models.CharField(max_length=400)

    # Delete 'FeedFolder' if the user who created them is deleted
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        # To prevent the user from making multiple folders with the same name
        unique_together = ('user', 'name')


# Note: Feeds are centralized and do not depend on a coexistence with a user
# For example, if a user deletes an account, the feed they imported should remain as a
# cache for other users. Additionally, This means if multiple users import the same feed url, only
# a single database entry is made for the feed - where both users reference the same item.
# Whenever an update request is made for the feed, it updates for all users using the shared url.
# We can also add a search where users can find and import from feeds that other users have already brought into the platform
class Feed(models.Model):
    # A feed may have a link pointing to the website that owns the feed (not the RSS url)
    link = models.URLField(blank=True)

    url = models.URLField(unique=True)

    # These will be the "true" name/description of the feed
    # RSS feeds typically provide this information
    # Sometimes the information isn't great, so the user can override this in "UserFeed"
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Some feeds have images, may be useful for styling purposes
    image_url = models.CharField(max_length=255, blank=True)
    # Private toggle to exclude this from the potential 'search' function
    private = models.BooleanField(default=False)

    # To keep track of when the feed was last updated.
    # feeds should be updated regularly but we don't want to update it if for example: it was already updated 5 seconds ago.
    last_updated = models.DateTimeField(default=timezone.now)

    # How often the feed should be updated (in minutes)
    ttl = models.IntegerField(default=10)


class UserFeed(models.Model):

    # UserFeed contains its own name and description, but defaults to the values from the feed
    # This is so that UserFeed can implement a custom name/description to user preference
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Delete 'UserFeed' if the user who created them is deleted
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Do not delete 'UserFeed' if their folder is deleted, feeds do not need a folder.
    folder = models.ForeignKey(
        FeedFolder,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # Do not delete the 'UserFeed' if the linked feed is deleted. (gives the user a chance to update the url)
    feed = models.ForeignKey(
        Feed,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def save(self, *args, **kwargs):
        # If the user did not provide a custom name or description, default to the feed values
        if not self.name:
            self.name = self.feed.name

        if not self.description:
            self.description = self.feed.description
        super().save(*args, **kwargs)

    class Meta:
        # FLAG: i assume this is the desired behaviour, but i could be wrong (will revisit if theres a problem).
        # Prevent the user from importing the same feed more than once
        unique_together = ('user', 'feed')
