# rss_app/models.py
from django.db import models
from folder_system.models import Folder

class FeedItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='rss_feed_items')

    def __str__(self):
        return self.title

