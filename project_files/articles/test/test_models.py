from django.utils import timezone
from ..models import Article
from feeds.models import Feed
from django.test import TestCase


class ArticleModelTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create(
            url='http://rss.cnn.com/rss/edition.rss', name='DCU')

        self.article = Article.objects.create(
            title='DCU News',
            link='http://example.com/dcu-news',
            publish_datetime=timezone.now()
        )

        self.article.feeds.add(self.feed)

    def test_article_creation(self):
        # Assert expected values for the article
        self.assertEqual(self.article.title, 'DCU News')
        self.assertEqual(self.article.link, 'http://example.com/dcu-news')
        self.assertIn(self.feed, self.article.feeds.all())

        # Check if the current date was correctly applied to the publish date
        now_timestamp = timezone.now().timestamp()
        feed_timestamp = self.article.publish_datetime.timestamp()

        # Delta here is the 'second tolerance'
        # So delta=1 means there's a 1 second tolerance for comparing the two timestamps
        # This is because a tiny amount of time will pass between the test creating the model and testing the timestamp.
        self.assertAlmostEqual(now_timestamp, feed_timestamp, delta=1)
