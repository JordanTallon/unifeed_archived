from django.dispatch import receiver
from feeds.signals import rss_feed_imported


@receiver(rss_feed_imported)
def import_articles_from_feed(sender, **kwargs):
    feed_url = kwargs.get('feed_url')
    if feed_url:
        print("Hello World")
