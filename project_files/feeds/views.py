from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .utils import *
from .serializers import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


@api_view(['POST'])
def importFeed(request):

    data = request.data

    # Check if a 'url' param was even given in the request data
    url = data.get('url')

    if not url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return Response({"error": "Invalid URL."}, status=status.HTTP_400_BAD_REQUEST)

    rss = read_rss_feed(url)

    if not rss:
        return Response({"error": "Unable to import an RSS feed for the given URL"}, status=status.HTTP_400_BAD_REQUEST)

    # Feedparse marks the rss as 'bozo' if the url contains incorrect rss data
    if rss.bozo:
        return Response({"error": "Malformed RSS feed. Unable to parse."}, status=status.HTTP_400_BAD_REQUEST)

    # Parse out relevant information within the 'feed' of the parsed RSS.
    rss_channel_data = read_rss_channel_elements(rss)

    # At minimum, the channel data should have a title and url.
    if 'title' not in rss_channel_data or 'link' not in rss_channel_data:
        return Response({"error": "No title or link in RSS feed"}, status=status.HTTP_400_BAD_REQUEST)

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

    serialized_feed = FeedSerializer(feed).data

    return Response({"message": "RSS Feed imported succesfully.", "Imported Feed": serialized_feed}, status=status.HTTP_201_CREATED)
