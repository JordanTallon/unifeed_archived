from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import FeedFolder, Feed, UserFeed, Article
from django.utils import timezone

User = get_user_model()


class FeedFolderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='tester123', password='@testing12345')


class FeedModelTest(TestCase):
    pass


class UserFeedModelTest(TestCase):
    pass


class ArticleModelTest(TestCase):
    pass
