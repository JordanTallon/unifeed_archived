from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import *
from articles.models import Article
from .utils import *
from .serializers import *
from .signals import rss_feed_imported


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

    try:
        rss = read_rss_feed(url)
    except ValueError as e:
        raise ValueError(f"Error fetching RSS feed: {e}")

    if not rss:
        raise ValueError("Unable to import an RSS feed for the given URL")

    # Feedparse marks the rss as 'bozo' if the url contains incorrect rss data
    if rss.bozo:
        raise ValueError("Unable to parse an RSS feed at the given URL")

    # Parse out relevant information within the 'feed' of the parsed RSS.
    rss_channel_data = read_rss_channel_elements(rss)

    feed = Feed.objects.create(
        url=url,
        link=rss_channel_data.get('link'),
        name=rss_channel_data.get('title'),
        description=rss_channel_data.get('description'),
        image_url=rss_channel_data.get('image_url'),
        ttl=rss_channel_data.get('ttl'),
    )

    feed.save()

    rss_feed_imported.send(sender=import_rss_feed,
                           rss=rss, rss_channel_data=rss_channel_data, feed=feed)

    return feed


@api_view(['POST'])
@login_required
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
@login_required
def import_user_feed(request):

    data = request.data

    # Make sure that both a url and user were provided in the data
    url = data.get('url')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

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


@login_required
def view_folder(request, user_id, folder_id):
    User = get_user_model()

    folder = get_object_or_404(FeedFolder, pk=folder_id)
    user = get_object_or_404(User, pk=user_id)
    userfeeds = UserFeed.objects.filter(user=user, folder=folder)

    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this folder.")

    repeat_times = range(3)
    return render(request, 'feeds/view_feed.html', {'folder': folder, 'userfeeds': userfeeds, 'repeat': repeat_times})


@login_required
def view_userfeed(request, user_id, folder_id,  userfeed_id=None):
    User = get_user_model()

    folder = get_object_or_404(FeedFolder, pk=folder_id)
    user = get_object_or_404(User, pk=user_id)
    folder_userfeeds = UserFeed.objects.filter(user=user, folder=folder)

    if request.user != user:
        return HttpResponseForbidden("You are not authorized to view this folder.")

    # If an ID was present
    if userfeed_id:
        # Find the userfeed associated with that ID and return the articles in it
        userfeed = get_object_or_404(
            UserFeed, user=user, folder=folder, pk=userfeed_id)
        userfeed_articles = Article.objects.filter(feeds__in=[userfeed.feed])
    else:
        # If no userfeed ID was present, get all userfeeds within the folder, and return all their articles.
        userfeed = None
        userfeed_articles = Article.objects.filter(
            feeds__in=folder_userfeeds.values_list('feed', flat=True))

    return render(request, 'feeds/view_feed.html', {
        'folder': folder,
        'folder_userfeeds': folder_userfeeds,
        'userfeed': userfeed,
        'userfeed_articles': userfeed_articles,
    })
