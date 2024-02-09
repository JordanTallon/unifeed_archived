from django.db import models
from feeds.models import Feed


class Article(models.Model):

    # Required
    title = models.CharField(max_length=255)
    link = models.URLField()

    # Optional (but really nice to have for visual purposes)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, default='')
    publish_date = models.DateField(blank=True, null=True)
    # Publisher would be nice to display. can be read from the title of the 'owning' rss feed?
    publisher = models.CharField(max_length=255, blank=True, default='')

    # Delete 'Article' if the RSS it was pulled from is deleted
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE
    )
