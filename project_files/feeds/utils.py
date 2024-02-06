import feedparser


def read_rss_feed(rss_url):
    # Use feedparser to parse the RSS feed
    rss_object = feedparser.parse(rss_url)
    # Return just the RSS_Object for now
    return rss_object


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