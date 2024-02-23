from rest_framework import serializers
from .models import FeedFolder, Feed, UserFeed


class FeedFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedFolder
        fields = ['id', 'name', 'user']


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'url', 'name',
                  'description', 'private', 'last_updated']


class UserFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeed
        fields = ['id', 'name', 'description', 'user', 'folder', 'feed']
