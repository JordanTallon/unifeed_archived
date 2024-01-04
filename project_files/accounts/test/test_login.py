from django.test import TestCase
from ..forms import UserLoginForm
from ..models import User
from http import HTTPStatus
from django.urls import reverse


class LoginTest(TestCase):

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

    # Test if the view correctly returns the 'login' page for the 'login' route
    def test_login_page_correct_response(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Ensure that the login form has a username and password field
    def test_user_login_form_has_expected_fields(self):
        self.assertTrue(issubclass(self.form_class, UserLoginForm))
        self.assertTrue('username' in self.form_class.Meta.fields)
        self.assertTrue('password' in self.form_class.Meta.fields)

    def test_login_with_invalid_user(self):
        user_data = {
            'username': '--',  # Invalid username
            'password': self.password
        }

        response = self.client.post(reverse('login'), user_data)

        # The user remains on the login page
        self.assertEqual(response.status_code, 200)

        # An error message is displayed to the user
        self.assertContains(
            response, 'Please enter a correct username and password.')

        # The user is not logged in
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_with_valid_user(self):
        user_data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(reverse('login'), user_data)

        # The user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)

        # The login page redirected to the home page after successful login
        self.assertRedirects(response, reverse('home'))
