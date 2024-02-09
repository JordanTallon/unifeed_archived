import feedparser


def read_rss_feed(rss_url):
    # Use feedparser to parse the RSS feed
    rss_object = feedparser.parse(rss_url)

    # Check if feedparser had a problem fetching the feed
    if hasattr(rss_object, 'status') and rss_object.status != 200:
        raise ValueError(
            f"Failed to fetch {rss_url}. HTTP status code: {rss_object.status}")

    return rss_object


# Extracts and returns 'meta data' from the feed
def read_rss_channel_elements(rss):
    feed = rss.feed

    channel_elements = {
        'title': feed.get('title', ''),
        'description': feed.get('subtitle', ''),
        'link': feed.get('link', ''),
        'image_url': feed.get('image', {}).get('href', '') if feed.get('image') else '',
        'last_updated': feed.get('updated', ''),
        'ttl': feed.get('ttl', ''),
    }

    return channel_elements


# Extracts and returns only relevant data from the entries
def clean_rss_entries(rss_entries):
    clean_entries = []
    for entry in rss_entries:
        clean_entry = {
            # Note: I have seen alternative field names for essentially the same thing
            # This is why fields like description have a "daisy chain" of entry gets
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'description': entry.get('description', entry.get('summary', '')),
            'image_url': entry.get('media_content', {})[0],
            'author': entry.get('author', ''),
            'published': entry.get('published', ''),
        }

        clean_entries.append(clean_entry)
    return clean_entries


# Temporary function for development
# Helps to examine the contents of an RSS feed to update the reading functions
# For example, we can find field name patterns in here to include in the clean_entry daisy chain
def debug_examine_rss_feed(rss_url):
    rss = read_rss_feed(rss_url)
    for entry in rss.entries:
        print(entry.keys())
