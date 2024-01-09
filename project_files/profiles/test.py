from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from accounts.models import User
from accounts.forms import UserLoginForm

class UserProfileTestCase(TestCase):
    # Initial account set up that can be used for each test
    def setUp(self) -> None:
        self.form_class = UserLoginForm
        self.username = "testaccount123"
        self.email = "test@example.com"
        self.password = "TestPassword99"

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_user_profile_creation(self):
        # Create a UserProfile instance for the test user
        profile = UserProfile.objects.create(user=self.user, bio='Test Bio')

        # Check if the UserProfile instance is created successfully
        self.assertIsInstance(profile, UserProfile)

        # Check if the user field is set correctly
        self.assertEqual(profile.user, self.user)

        # Check if the bio field is set correctly
        self.assertEqual(profile.bio, 'Test Bio')

    def test_user_profile_blank_bio(self):
        # Create a UserProfile instance for the test user without a bio
        profile = UserProfile.objects.create(user=self.user)

        # Check if the bio field is blank
        self.assertEqual(profile.bio, '')

    # Add more test cases for any additional fields you may have added to the UserProfile model
