from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .utils import *
from .serializers import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def import_rss_feed(url):

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

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
        feed = import_rss_feed(url)
        serialized_feed = FeedSerializer(feed).data
        return Response({"message": "RSS Feed imported successfully.", "Imported Feed": serialized_feed}, status=status.HTTP_201_CREATED)
    except ValidationError:
        return Response({"error": "Invalid URL."}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
