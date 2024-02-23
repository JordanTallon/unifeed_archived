from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ..models import User
from articles.models import RecentlyRead
from articles.test.factories import ArticleFactory


class UserModelTest(TestCase):
    def test_user_model_exists(self):
        users = User.objects.count()
        self.assertEqual(users, 0)

    def test_add_new_user(self):
        user = User.objects.create_user(
            username='test', email="test@example.com", password='hello_world')
        user.save()

        added_user = User.objects.first()

        self.assertIsNotNone(added_user)

        self.assertEqual(added_user.username, "test",
                         "Username for new User is correctly set")

        self.assertEqual(added_user.email, "test@example.com",
                         "Email for new User is correctly set")

        self.assertTrue(added_user.check_password("hello_world"),
                        "Password for new user is correctly set")

    def test_user_with_invalid_email_raises_error(self):
        user = User.objects.create_user(username="test", email="invalid-email")

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_unique_username_constraint(self):
        User.objects.create_user(
            username='unique', email="test@example.com")

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='unique', email="newtest@example.com")

    def test_unique_email_constraint(self):
        User.objects.create_user(
            username='test', email="unique@example.com")

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='test2', email="unique@example.com")

    def test_user_track_history_default_false(self):
        user = User.objects.create_user(
            username='test', email="test@example.com")

        self.assertFalse(user.track_history)

    def test_track_history_disable_deletes_articles(self):
        user = User.objects.create_user(
            username='test', email="test@example.com", track_history=True)

        # Create 3 fake articles to add to read history
        articles = ArticleFactory.create_batch(3)

        # Create a RecentlyRead object for earch article to associate with the user
        for article in articles:
            RecentlyRead.objects.create(article=article, user=user)

        # Count articles in user read history
        history_count = len(RecentlyRead.objects.filter(user=user))

        # Assert that the 3 articles are in the user history
        self.assertEqual(history_count, 3)

        # Disable history tracking for the user
        user.track_history = False
        user.save()

        # Get articles in user read history
        history = RecentlyRead.objects.filter(user=user)

        # Assert that there are no articles in the user history
        self.assertFalse(history)
