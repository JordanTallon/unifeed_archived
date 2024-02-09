from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .utils import *
from .serializers import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404


def import_rss_feed(url):

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
    except:
        raise ValueError("Invalid URL.")

    # Check if the feed already exists, return it if so.
    existing_feed = Feed.objects.filter(url=url).first()
    if existing_feed:
        return existing_feed

    rss = read_rss_feed(url)

    if not rss:
        raise ValueError("Unable to import an RSS feed for the given URL")

    # Feedparse marks the rss as 'bozo' if the url contains incorrect rss data
    if rss.bozo:
        raise ValueError("Unable to parse an RSS feed at the given URL")

    # Parse out relevant information within the 'feed' of the parsed RSS.
    rss_channel_data = read_rss_channel_elements(rss)

    # At minimum, the channel data should have a title and url.
    if 'title' not in rss_channel_data or 'link' not in rss_channel_data:
        raise ValueError("No title or link in RSS feed")

    feed = Feed.objects.create(
        url=url,
        link=rss_channel_data.get('link'),
        name=rss_channel_data.get('title'),
        description=rss_channel_data.get('description') if rss_channel_data.get(
            'description', '') != '' else None,

        image_url=rss_channel_data.get('image_url') if rss_channel_data.get(
            'image_url', '') != '' else None,

        ttl=rss_channel_data.get('ttl') if rss_channel_data.get(
            'ttl', '') != '' else None,
    )

    feed.save()

    return feed


@api_view(['POST'])
def import_new_feed(request):

    data = request.data

    # Check if a 'url' param was even given in the request data
    url = data.get('url')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        feed = import_rss_feed(url)
        serialized_feed = FeedSerializer(feed).data
        return Response({"message": "RSS Feed imported successfully.", "Imported Feed": serialized_feed}, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def import_user_feed(request):

    data = request.data

    # Make sure that both a url and user were provided in the data
    url = data.get('url')
    user = data.get('user')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    if not user:
        return Response({"error": "A User is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the given user exists
    User = get_user_model()

    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the feed is valid or already in the database (can reuse it from another user)
    feed = None
    try:
        feed = import_rss_feed(url)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the UserFeed already exists, return it if so.
    existing_feed = UserFeed.objects.filter(feed=feed, user=user).first()
    if existing_feed:
        serialized_feed = UserFeedSerializer(existing_feed).data
        return Response({"message": "Existing UserFeed found.", "UserFeed": serialized_feed})

    # Create and return the new user feed
    user_feed = UserFeed.objects.create(feed=feed, user=user)
    serialized_feed = UserFeedSerializer(user_feed).data
    return Response({"message": "RSS Feed assigned to user successfully.", "Userfeed": serialized_feed}, status=status.HTTP_201_CREATED)


def view_folder(request, user_id, folder_id):
    User = get_user_model()

    folder = get_object_or_404(FeedFolder, pk=folder_id)
    user = get_object_or_404(User, pk=user_id)
    feeds = UserFeed.objects.filter(user=user, folder=folder)

    return render(request, 'feeds/view_feed.html', {'folder': folder, 'feeds': feeds})
