from django.test import TestCase
from ..forms import UserLoginForm
from ..models import User
from http import HTTPStatus
from django.urls import reverse


class LoginTest(TestCase):

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

    def test_login_page_correct_response(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_login_form_has_expected_fields(self):
        self.assertTrue(issubclass(self.form_class, UserLoginForm))
        self.assertTrue('username' in self.form_class.Meta.fields)
        self.assertTrue('password' in self.form_class.Meta.fields)

    def test_login_with_valid_user(self):
        user_data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(reverse('login'), user_data)

        self.assertRedirects(response, reverse('home'))
