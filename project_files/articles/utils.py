import email.utils
import datetime
from django.utils import timezone
from .models import Article
from bs4 import BeautifulSoup


def strip_html(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text()

# Extracts and returns only relevant article data from the entries


def clean_rss_entries(rss_entries, rss_header):

    clean_entries = []
    for entry in rss_entries:
        # If the media_content is present, check if its a list of different images
        # if so, just use the first image.
        if 'media_content' in entry:
            if isinstance(entry['media_content'], list):
                entry['media_content'] = entry['media_content'][0].get(
                    'url')

        clean_entry = {
            # Note: These entries are already normalized by feedparser.
            # But since we are handling lots of different feeds, the entries can heavily vary.
            'title': entry.get('title', 'Failed to load title.'),
            'link': entry.get('link', 'Failed to load link.'),
            'description': entry.get('summary', ''),
            'author': entry.get('author', ''),
            'image_url': entry.get('media_content', ''),
        }

        # If no image was found, default to using the rss feed's image (may also be none)
        if clean_entry['image_url'] == '':
            clean_entry['image_url'] = rss_header['image_url']

        # As a last resort, generate a placeholder image for the article displaying the feeds name
        if clean_entry['image_url'] == '':
            clean_entry[
                'image_url'] = f"https://placehold.co/600x400/dfdfdf/FFF?text={ rss_header['title'] }&font=roboto"

        parsed_datetime = None

        # Check if feedparser was able to parse a datetime automatically, if not, parse our own.
        if entry.get('published_parsed'):
            try:
                entry_time = entry.get('published_parsed')
                parsed_datetime = datetime.datetime(
                    year=entry_time.tm_year,
                    month=entry_time.tm_mon,
                    day=entry_time.tm_mday,
                    hour=entry_time.tm_hour,
                    minute=entry_time.tm_min,
                    second=entry_time.tm_sec
                )
            except Exception as e:
                print(f"Error parsing 'published_parsed': {e}")
        # No parsed published was found, parse the published datetime if it exists instead
        # its safe to assume it's an rfc882 datetime.
        # See rfc882_date_to_python_datetime comments for more information
        elif entry.get('published'):
            try:
                parsed_datetime = rfc882_date_to_python_datetime(
                    entry.get('published'))
            except Exception as e:
                print(f"Error parsing 'published': {e}")

        # Make the parsed datetime timezone aware
        if parsed_datetime and not timezone.is_aware(parsed_datetime):
            parsed_datetime = timezone.make_aware(
                parsed_datetime, timezone=timezone.get_current_timezone())

        clean_entry['publish_datetime'] = parsed_datetime

        # Handle database limitations
        # Get max lengths for CharFields in Article model
        title_max_length = Article._meta.get_field('title').max_length
        author_max_length = Article._meta.get_field('author').max_length
        link_max_length = Article._meta.get_field('link').max_length

        if len(clean_entry['link']) > link_max_length:
            # Sadly a link cannot be truncated without losing the validity of the url.
            # For now, just skip this entry due to technical limitations.
            # In the future, I will research alternative procedures, top of my head:
            # 1. Implementing a URL shortener / redirector
            # 2. Futhering investigation into pushing the character limits of Djangos URLField.
            continue

        # Truncate any fields above their max length.
        if len(clean_entry['title']) > title_max_length:
            # Truncate the title at max_length -3 characters (to make room for 3 ellipsis for styling)
            clean_entry['title'] = clean_entry['title'][:title_max_length-3] + '...'
        clean_entry['author'] = clean_entry['author'][:author_max_length]
        # clean_entry['publisher'] = clean_entry['publisher'][:publisher_max_length]

        # Strip out any HTML found in the description and title (some RSS feeds provide HTML, which we don't want)
        clean_entry['description'] = strip_html(clean_entry['description'])
        clean_entry['title'] = strip_html(clean_entry['title'])

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
