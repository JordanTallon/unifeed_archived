from feeds.signals import rss_feed_imported
from django.dispatch import receiver
from .models import Article


@receiver(rss_feed_imported)
def import_articles_from_feed(sender, **kwargs):

    print("Signal received")

    rss_entries = kwargs.get('rss_entries')
    feed = kwargs.get('feed')

    for entry in rss_entries:
        new_article = Article.objects.create(
            title=entry['title'], link=entry['link'], feed=feed)

        if entry['description'] != '':
            new_article.description = entry['description']

        if entry['image_url'] != '':
            new_article.image_url = entry['image_url']

        if entry['author'] != '':
            new_article.author = entry['author']

        if entry['published'] != '':
            new_article.published = entry['published']

        new_article.save()
