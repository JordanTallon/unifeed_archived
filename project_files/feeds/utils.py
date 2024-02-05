import feedparser


def read_rss_feed(rss_url):
    # Use feedparser to parse the RSS feed
    feed = feedparser.parse(rss_url)
    items = feed.entries

    for item in items:
        title = item.title if hasattr(item, 'title') else 'No title'
        description = item.description if hasattr(
            item, 'description') else 'No description'
        link = item.link if hasattr(item, 'link') else 'No link'

        new_feed = FeedItem(
            title=title,
            description=description,
            link=link,
            folder_id=folder_id
        )

        new_feed.save()
