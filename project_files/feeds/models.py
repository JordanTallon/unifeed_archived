from django.db import models
from django.conf import settings
from django.utils import timezone

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

    def __str__(self):
        return self.name


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

    # Extracted from the link e.g. https://www.vox.com : Vox 'publisher'
    publisher = models.CharField(max_length=255, blank=True)

    # To keep track of when the feed was last updated.
    # feeds should be updated regularly but we don't want to update it if for example: it was already updated 5 seconds ago.
    last_updated = models.DateTimeField(default=timezone.now)

    # How often the feed should be updated (in minutes)
    ttl = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    # A relative time since last_updated (i.e. '7 days ago', '2 hours ago', 'just now')
    def time_since_update(self):

        now = timezone.now()

        try:
            difference = now - self.last_updated

            days = difference.days
            weeks = days // 7
            months = days // 30

            if months > 0:
                return f"{months} months ago"

            if weeks > 0:
                return f"{weeks} weeks ago"

            if days > 1:
                return f"{days} days ago"

            if days == 1:
                return f"{days} day ago"

            mins = difference.seconds // 60

            if mins >= 60:
                hours = mins // 60
                return f"{hours} hours ago"

            if mins >= 1:
                return f"{mins} minutes ago"

            return "Just now."
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


class UserFeed(models.Model):

    # UserFeed contains its own name and description, but defaults to the values from the feed
    # This is so that UserFeed can implement a custom name/description to user preference
    name = models.CharField(max_length=255, blank=True)
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

    # Delete the userfeed if the original feed is deleted. In the future, check ways to preserve the userfeed and notify the user to update the url.
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        # If the user did not provide a custom name or description, default to the feed values
        if not self.name or self.name == '':
            self.name = self.feed.name

        if not self.description:
            self.description = self.feed.description

        if self.name == '':
            self.name = 'Unnamed Feed'

        super().save(*args, **kwargs)

    class Meta:
        # Prevent the user from importing the same feed more than once into the same folder
        unique_together = ('user', 'feed', 'folder')
