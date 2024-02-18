import feedparser
from django.core.validators import URLValidator
from .models import Feed
from .signals import rss_feed_imported
from django.utils import timezone
import tldextract


def import_rss_feed(url):

    # Verify that the 'url' param contained a genuine URL
    validate = URLValidator()
    try:
        validate(url)
    except:
        raise ValueError("Invalid URL.")

    # Check if a feed already exists with the RSS url, if not create it
    feed, created = Feed.objects.get_or_create(
        url=url
    )

    try:
        rss, rss_channel_data = parse_rss_feed(url)
    except Exception as e:
        raise ValueError("Error in parsing RSS feed: " + str(e))

    # Update the feed object with the rss_channel_data and save it
    save_feed(feed, rss_channel_data)

    # Send a signal to import articles from the feed
    rss_feed_imported.send(sender=import_rss_feed,
                           rss=rss, rss_channel_data=rss_channel_data, feed=feed)

    return feed, created


def save_feed(feed, rss_channel_data):
    feed.link = rss_channel_data.get('link', feed.link)
    feed.name = rss_channel_data.get('title', feed.name)
    feed.description = rss_channel_data.get('description', feed.description)
    feed.image_url = rss_channel_data.get('image_url', feed.image_url)
    feed.ttl = rss_channel_data.get('ttl', feed.ttl)
    feed.publisher = rss_channel_data.get('publisher', feed.publisher)
    feed.last_updated = timezone.now()
    feed.save()


def parse_rss_feed(url):
    try:
        rss = read_rss_feed(url)
    except ValueError as e:
        raise ValueError(f"Error fetching RSS feed: {e}")

    # Parse out relevant information within the 'feed' of the parsed RSS.
    rss_channel_data = read_rss_channel_elements(rss)

    return rss, rss_channel_data


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

    if channel_elements['link'] != '':
        website_tld = tldextract.extract(channel_elements['link'])
        subdomain = website_tld.subdomain + "."

        # Subdomains we don't want to included (we want stuff like news.cnn to be included or abcnews.go etc)
        # But not stuff like www.fox, this list will be manually added to as undesired publisher names appear
        exclude_subdomains = {'www', 'm', 'ftp', 'mail', 'webmail', 'blog', 'cdn',
                              'static', 'api', 'secure', 'dev', 'development',
                              'staging', 'admin'}

        if subdomain and subdomain in exclude_subdomains:
            subdomain = ''

        domain = website_tld.domain
        channel_elements['publisher'] = subdomain.capitalize() + \
            domain.capitalize()

    return channel_elements


# Temporary function for development
# Helps to examine the contents of an RSS feed to update the reading functions
# For example, we can find field name patterns in here to include in the clean_entry daisy chain
def debug_examine_rss_feed(entries):
    for entry in entries:
        print(entry.keys())
