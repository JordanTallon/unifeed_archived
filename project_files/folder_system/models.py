# folder_system/models.py
from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FeedItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

