from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import FeedFolder, Feed, UserFeed, Article
from django.utils import timezone

User = get_user_model()


class FeedFolderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='tester123', password='@testing12345')

    def test_user_create_folder(self):
        folder = FeedFolder.objects.create(name='Space', user=self.user)
        # Assert that the folder is correctly named
        self.assertEqual(folder.name, 'Space')

        # Assert that the folder is owned by the creating user
        self.assertEqual(folder.user, self.user)

    def test_add_unique_folders(self):
        # Get the number of folders at the start
        folder_count_before = FeedFolder.objects.count()

        FeedFolder.objects.create(name='Space', user=self.user)
        FeedFolder.objects.create(name='Technology', user=self.user)

        # Update current folder count
        folder_count = FeedFolder.objects.count()

        # Assert that 2 folders were succesfully added
        self.assertEqual(folder_count - folder_count_before, 2)

    def test_folder_name_must_be_unique(self):
        # Add Space folder
        FeedFolder.objects.create(name='Space', user=self.user)

        # Assert that adding the 'Space' folder a second time raises an error
        with self.assertRaises(Exception):
            FeedFolder.objects.create(name='Space', user=self.user)


class FeedModelTest(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create(
            url='http://rss.cnn.com/rss/edition.rss',
            name='CNN',
            description='CNN News Feed'
        )

    def test_feed_creation(self):
        self.assertEqual(self.feed.url, 'http://rss.cnn.com/rss/edition.rss')
        self.assertEqual(self.feed.name, 'CNN')
        # We didn't specify private in the creation, so it should default to false
        self.assertFalse(self.feed.private)

    def test_last_updated_default(self):
        now_timestamp = timezone.now().timestamp()
        feed_timestamp = self.feed.last_updated.timestamp()

        # Delta here is the 'second tolerance'
        # So delta=1 means there's a 1 second tolerance for comparing the two timestamps
        # This is because a tiny amount of time will pass between the test creating the model and testing the timestamp.
        self.assertAlmostEqual(now_timestamp, feed_timestamp, delta=1)


class UserFeedModelTest(TestCase):
    def setUp(self):
        # Create both a user and feed object
        self.user = User.objects.create(
            username='tester123', password='@testing12345')
        self.feed = Feed.objects.create(
            url='http://rss.cnn.com/rss/edition.rss',
            name='CNN',
            description='CNN News Feed'
        )

    def test_create_user_feed(self):
        # Get the count before the UserFeed is added
        before_count = UserFeed.objects.count()

        # Add the new User_Feed
        user_feed = UserFeed.objects.create(feed=self.feed, user=self.user)

        # Get the count after the UserFeed is added
        count = UserFeed.objects.count()

        # Assert that 1 new UserFeed was added to the count
        self.assertEqual(count - before_count, 1)

        # Check if the new user feed defaulted to the feed name and description
        self.assertEqual(user_feed.name, 'CNN')
        self.assertEqual(user_feed.description, 'CNN News Feed')

        # Assert that the original feed is being correctly referenced through UserFeed
        self.assertEqual(user_feed.feed.name, 'CNN')
        self.assertEqual(user_feed.feed.description, 'CNN News Feed')
        self.assertEqual(user_feed.feed.url,
                         'http://rss.cnn.com/rss/edition.rss')

    def test_user_feed_custom_name_and_description(self):

        # Add the new User_Feed
        user_feed = UserFeed.objects.create(
            feed=self.feed,
            user=self.user,
            name="Custom CNN",
            description="This description is way better than the default CNN one"
        )

        # Assert that custom values were succesfully applied
        self.assertEqual(user_feed.name, 'Custom CNN')
        self.assertEqual(user_feed.description,
                         'This description is way better than the default CNN one')


class ArticleModelTest(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create(
            url='http://rss.cnn.com/rss/edition.rss', name='DCU')

        self.article = Article.objects.create(
            title='DCU News',
            link='http://example.com/dcu-news',
            feed=self.feed,
            publish_date=timezone.now().date()
        )

    def test_article_creation(self):
        # Assert expected values for the article
        self.assertEqual(self.article.title, 'DCU News')
        self.assertEqual(self.article.link, 'http://example.com/dcu-news')
        self.assertEqual(self.article.feed, self.feed)

        # Check if the publish timestamp was correctly applied
        now_timestamp = timezone.now().timestamp()
        article_timestamp = self.article.publish_date

        # delta=1 means there's a 1 second tolerance for comparing the two timestamps
        self.assertAlmostEqual(now_timestamp, article_timestamp, delta=1)
