from django.test import TestCase, Client
from django.urls import reverse
from ..models import UserFeed, FeedFolder
from articles.models import Article
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from feeds.test.factories import UserFeedFactory
from django.contrib.auth import get_user_model


class ViewTests(TestCase):
    def setUp(self):

        self.client = Client()
        User = get_user_model()

        # Set up initial objects to be used in the tests
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create fake UserFeeds for the user
        self.userfeeds = UserFeedFactory.create_batch(3, user=self.user)

        # Get all feed ids from the fake UserFeeds
        feed_ids = [userfeed.feed.id for userfeed in self.userfeeds]

        # Get all articles associated with the feeds
        self.articles = list(Article.objects.filter(feed_id__in=feed_ids))

    def test_my_feed_view(self):

        # Test client and HTML response
        response = self.client.get(reverse('my_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feeds/my_feed.html')

        # Get all articles belonging to the user's feeds
        returned_articles = response.context['articles']

        # Assert that all articles belong to the user's feeds are in the returned articles
        self.assertEqual(sorted([a.id for a in returned_articles]),
                         sorted([a.id for a in self.articles]))
