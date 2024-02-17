import feedparser


def read_rss_feed(rss_url):
    # Use feedparser to parse the RSS feed
    rss_object = feedparser.parse(rss_url)

    # Check if feedparser had a problem fetching the feed
    if hasattr(rss_object, 'status') and rss_object.status != 200:
        raise ValueError(
            f"Failed to fetch {rss_url}. HTTP status code: {rss_object.status}")

    if not rss_object:
        raise ValueError("Unable to import an RSS feed for the given URL")

    # Feedparse marks the rss as 'bozo' if the url contains incorrect rss data
    if rss_object.bozo:
        raise ValueError("Unable to parse an RSS feed at the given URL")

    return rss_object


# Extracts and returns 'metadata' from the feed
def read_rss_channel_elements(rss):
    feed = rss.feed

    channel_elements = {
        'title': feed.get('title', ''),
        'description': feed.get('subtitle', ''),
        'link': feed.get('link', ''),
        'image_url': feed.get('image', ''),
        'last_updated': feed.get('updated', ''),
        'ttl': feed.get('ttl', '10'),
    }

    retrieved_image_url = channel_elements['image_url']
    if isinstance(retrieved_image_url, dict):
        channel_elements['image_url'] = retrieved_image_url.get('href', '')

    return channel_elements


# Temporary function for development
# Helps to examine the contents of an RSS feed to update the reading functions
# For example, we can find field name patterns in here to include in the clean_entry daisy chain
def debug_examine_rss_feed(entries):
    for entry in entries:
        print(entry.keys())
