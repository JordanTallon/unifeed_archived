import email.utils
import datetime
from django.utils import timezone

# Extracts and returns only relevant article data from the entries


def clean_rss_entries(rss_entries, rss_header):

    clean_entries = []
    for entry in rss_entries:
        clean_entry = {
            # Note: These entries are already normalized by feedparser.
            # But since we are handling lots of different feeds, the entries can heavily vary.
            'title': entry.get('title', 'Failed to load title.'),
            'link': entry.get('link', 'Failed to load link.'),
            'description': entry.get('summary', ''),
            'author': entry.get('author', ''),
            'image_url': entry.get('media_content', ''),
        }

        # If the media_content is a dictionary of different images, just use the first image.
        if isinstance(clean_entry['image_url'], dict):
            clean_entry['image_url'] = clean_entry['image_url'][0].get(
                'url')

        # If no image was found, default to using the rss feed's image
        if clean_entry['image_url'] == '':
            clean_entry['image_url'] = rss_header['image_url']

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
