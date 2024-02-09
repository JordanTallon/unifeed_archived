import feedparser
import email.utils
import datetime
from django.utils import timezone


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
    # debug_examine_rss_feed(rss_entries)
    clean_entries = []
    for entry in rss_entries:
        clean_entry = {
            # Note: I have seen alternative field names for essentially the same thing
            # This is why fields like description have a "daisy chain" of entry gets
            'title': entry.get('title', 'Failed to load title.'),
            'link': entry.get('link', 'Failed to load link.'),
            'description': entry.get('description', entry.get('summary', '')),
            'author': entry.get('author', ''),
        }

        # Try read an image_url from the first element of 'media_content'
        # I will track different rss feeds and see if the naming convention deviates from media_content
        # If so, I will handle the other conventional names too
        image_url = ''
        if 'media_content' in entry and len(entry['media_content']) > 0:
            image_url = entry['media_content'][0].get('url', '')
        clean_entry['image_url'] = image_url

        parsed_datetime = None

        # Check if feedparser was able to parse a datetime automatically, if not, parse our own.
        if entry.get('published_parsed'):
            entry_time = entry.get('published_parsed')
            parsed_datetime = datetime.datetime(
                year=entry_time.tm_year,
                month=entry_time.tm_mon,
                day=entry_time.tm_mday,
                hour=entry_time.tm_hour,
                minute=entry_time.tm_min,
                second=entry_time.tm_sec
            )
        else:
            # No parsed published was found, parse the published datetime if it exists instead
            # its safe to assume it's an rfc882 datetime.
            # See rfc882_date_to_python_datetime comments for more information
            if entry.get('published'):
                parsed_datetime = rfc882_date_to_python_datetime(
                    entry.get('published'))

        # Make the parsed datetime timezone aware
        if parsed_datetime and not timezone.is_aware(parsed_datetime):
            parsed_datetime = timezone.make_aware(
                parsed_datetime, timezone=timezone.get_current_timezone())

        clean_entry['publish_datetime'] = parsed_datetime

        clean_entries.append(clean_entry)
    return clean_entries


# All date-times in RSS conform to the Date and Time Specification of RFC 822,
# with the exception that the year may be expressed with two characters or four characters (four preferred).
# Source: RSS2.0 Specification - https://cyber.harvard.edu/rss/rss.html
# This means its safe to assume all dates in an RSS feed are RFC 822 formatted.
# The problem is, Django prefers python Datetime. Easiest solution is to convert all rfc882 dates into a Python Datetime
# After doing some research, I stumbled upon the email.utils module https://docs.python.org/3/library/email.utils.html
# Luckily this handles the conversion for us, but I will still seperate the logic into this function to create visiblity
# of the issue and provide a centralized location to easily change the parse, if the email.utils function can no longer be relied upon
def rfc882_date_to_python_datetime(rfc882_date):
    return email.utils.parsedate_to_datetime(rfc882_date)


# Temporary function for development
# Helps to examine the contents of an RSS feed to update the reading functions
# For example, we can find field name patterns in here to include in the clean_entry daisy chain
def debug_examine_rss_feed(entries):
    for entry in entries:
        print(entry.keys())
