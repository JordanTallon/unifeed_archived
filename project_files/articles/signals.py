from feeds.signals import rss_feed_imported
from django.dispatch import receiver
from .models import Article


@receiver(rss_feed_imported)
def import_articles_from_feed(sender, **kwargs):

    rss_entries = kwargs.get('rss_entries')
    feed = kwargs.get('feed')

    for entry in rss_entries:
        # Check if an article with this link already exists
        # The pre-existing condition is that the article url and title are the exact same as the 'new' one
        article, created = Article.objects.get_or_create(
            link=entry['link'],
            title=entry['title'],
        )

        # If the article is new, set its values
        if created:
            article.description = entry.get('description', '')
            article.image_url = entry.get('image_url', '')
            article.author = entry.get('author', '')
            article.publish_datetime = entry.get('publish_datetime', None)
            article.save()
        else:
            # Add the current feed to the existing article's potentially many feeds
            article.feeds.add(feed)
