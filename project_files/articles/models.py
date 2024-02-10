from django.db import models
from feeds.models import Feed


class Article(models.Model):

    # Required
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=500)

    # Optional (but really nice to have for visual purposes)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, default='')
    publish_datetime = models.DateTimeField(blank=True, null=True)
    # Publisher would be nice to display. can be read from the title of the 'owning' rss feed?
    publisher = models.CharField(max_length=255, blank=True, default='')

    # Many feeds can use the same article. For example, Fox news may have a Breaking News feed, and a Politics feed.
    # These feeds may present the same article, in that case we want both feeds to share the same database object for reusability.
    # This allows for a better use of system resources and storage.
    feeds = models.ManyToManyField(Feed)
