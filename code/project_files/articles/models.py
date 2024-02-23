from django.db import models
from feeds.models import Feed
from datetime import datetime
from django.utils import timezone
from django.conf import settings


class Article(models.Model):

    # Required
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=500)

    # Optional (but really nice to have for visual purposes)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, default='')
    publish_datetime = models.DateTimeField(blank=True, null=True)

    # The feed this article belongs to
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        default=None
    )

    # A shorter version of the description for displaying in HTML for an article preview

    def preview_description(self):
        word_limit = 15
        words = self.description.split()
        if len(words) > word_limit:
            return ' '.join(words[:word_limit]) + '...'
        else:
            return self.description

    # A relative time since the publish_datetime (i.e. '7 days ago', '2 hours ago', 'just now')
    def time_since(self):

        now = timezone.make_aware(
            datetime.now(), timezone=timezone.get_current_timezone())

        try:
            difference = now - self.publish_datetime

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


class SavedArticle(models.Model):
    # The article being saved
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    # The user saving the article
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # When the article was saved
    saved_at = models.DateTimeField(auto_now_add=True)


class RecentlyRead(models.Model):
    # The article being saved
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    # The user that recently read the article
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # When the article was read
    read_at = models.DateTimeField(auto_now_add=True)
