from django.test import TestCase
from ..forms import UserLoginForm
from ..models import User
from http import HTTPStatus
from django.urls import reverse


class LogoutTest(TestCase):

    # Initial account set up that can be used for each test
    def setUp(self) -> None:
        self.form_class = UserLoginForm
        self.username = "testaccount123"
        self.email = "test@example.com"
        self.password = "TestPassword99"

        User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_logout_view_logs_user_out(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

        # Check if the user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)

        # Call logout view
        self.client.get(reverse('logout'))

        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)
