# rss_app/models.py
from django.db import models
from folder_system.models import Folder
from django.urls import reverse

class FeedItem(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    link = models.URLField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='rss_feed_items')

    def get_absolute_url(self):
        if self.folder:
            return reverse('feeds_in_folder', args=[str(self.folder.id)])
        else:
            return reverse('index')  

    def __str__(self):
        return self.title
