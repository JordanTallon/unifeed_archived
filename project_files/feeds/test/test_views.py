from django.test import TestCase, Client
from django.urls import reverse
from ..models import UserFeed, FeedFolder, Feed
from articles.models import Article
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from feeds.test.factories import UserFeedFactory, FeedFolderFactory
from django.contrib.auth import get_user_model


class ViewTests(TestCase):
    def setUp(self):

        self.client = Client()
        User = get_user_model()

        # Set up initial objects to be used in the tests
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create a fake folder for testing
        self.folder = FeedFolderFactory(user=self.user)

        # Create fake UserFeeds for the user
        self.userfeeds = UserFeedFactory.create_batch(3, user=self.user)

        # Get all feed ids from the fake UserFeeds
        feed_ids = [userfeed.feed.id for userfeed in self.userfeeds]
        self.feeds = list(Feed.objects.filter(id__in=feed_ids))

        # Single feed for testing
        self.feed = self.feeds[0]

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

    def test_get_add_user_feed_to_folder(self):
        # get request returns the correct response / HTML
        response = self.client.get(
            reverse('add_user_feed_to_folder', args=[self.folder.name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feeds/add_new_feed.html')

    def test_post_add_user_feed_to_folder_with_valid_data(self):
        # Test POST request with valid form data
        form_data = {'feed': self.feed.id}

        # Get original count of UserFeeds
        original_count = UserFeed.objects.count()

        response = self.client.post(
            reverse('add_user_feed_to_folder', args=[self.folder.name]), form_data)

        # Assert that a new userfeed was added
        self.assertEqual(UserFeed.objects.count(), original_count + 1)

        # get the newly created UserFeed ID
        new_userfeed = UserFeed.objects.latest('id')
        userfeed_id = new_userfeed.id

        # Make sure the user was redirected to view the new feed
        self.assertRedirects(response, reverse('view_userfeed', args=[
                             self.user.id, self.folder.id, userfeed_id]))

    def test_post_add_user_feed_to_folder_with_invalid_data(self):

        # Get original count of UserFeeds
        original_count = UserFeed.objects.count()

        # Test POST request with invalid data
        form_data = {'feed': ''}
        response = self.client.post(
            reverse('add_user_feed_to_folder', args=[self.folder.name]), form_data)

        # ASsert that the invalid feed was not added
        self.assertEqual(UserFeed.objects.count(), original_count)

        # Assert OK response and correct html returned
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feeds/add_new_feed.html')

    def test_post_add_duplicate_user_feed_to_folder(self):
        # Add the new UserFeed to the folder
        form_data = {'feed': self.feed.id}
        self.client.post(reverse('add_user_feed_to_folder',
                         args=[self.folder.name]), form_data)

        # Get original count of UserFeeds
        original_count = UserFeed.objects.count()

        # Attempt to add duplicate UserFeed
        response = self.client.post(
            reverse('add_user_feed_to_folder', args=[self.folder.name]), form_data)

        # The count should remain the same
        self.assertEqual(UserFeed.objects.count(), original_count)

        # Check for an error message in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("already contains this feed" in str(message)
                        for message in messages))
