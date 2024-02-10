from feeds.signals import rss_feed_imported
from django.dispatch import receiver
from .models import Article
from .utils import clean_rss_entries


@receiver(rss_feed_imported)
def import_articles_from_feed(sender, **kwargs):

    rss = kwargs.get('rss')
    rss_channel_data = kwargs.get('rss_channel_data')
    feed = kwargs.get('feed')

    rss_entries = clean_rss_entries(rss.entries, rss_channel_data)
    for entry in rss_entries:
        # Check if an article with this link already exists
        # The pre-existing condition is that the article url and title are the exact same as the 'new' one
        article, created = Article.objects.get_or_create(
            link=entry['link'],
            title=entry['title'],
        )

        # If the article is new, set its values
        if created:
            article.description = entry['description']
            article.image_url = entry['image_url']
            article.author = entry['author']
            article.publish_datetime = entry['publish_datetime']
            article.save()
            article.feeds.add(feed)
        else:
            if not article.feeds.filter(id=feed.id).exists():
                article.feeds.add(feed)
