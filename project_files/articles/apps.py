from django.apps import AppConfig
from feeds.signals import rss_feed_imported


def import_articles_from_feed(sender, **kwargs):
    rss_entries = kwargs.get('rss_entries')
    if rss_entries:
        for item in rss_entries:
            print(item)


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        rss_feed_imported.connect(import_articles_from_feed)
