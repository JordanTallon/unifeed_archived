from django.test import TestCase
from ..forms import UserRegistrationForm
from ..models import User
from http import HTTPStatus
from django.urls import reverse


class RegistrationTest(TestCase):
    # Runs at the start of the test
    def setUp(self) -> None:
        self.form_class = UserRegistrationForm

    def test_registration_page_correct_response(self):
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'accounts/registration.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_registration_form_has_expected_fields(self):
        self.assertTrue(issubclass(self.form_class, UserRegistrationForm))
        self.assertTrue('username' in self.form_class.Meta.fields)
        self.assertTrue('email' in self.form_class.Meta.fields)
        self.assertTrue('password1' in self.form_class.Meta.fields)
        self.assertTrue('password2' in self.form_class.Meta.fields)
        self.assertTrue('track_analytics' in self.form_class.Meta.fields)

    # Test to assure that the form works when given valid data
    def test_user_registration_form_succesful_validation(self):
        sample_data = {
            "username": "TestAccount",
            "email": "test@example.com",
            "password1": "33Test1234",
            "password2": "33Test1234",
            "track_analytics": False
        }

        form = self.form_class(sample_data)

        self.assertTrue(form.is_valid())

    # Test to check if the form succesfully passes information to the database
    def test_user_registration_form_writes_to_database(self):
        sample_data = {
            "username": "TestAccount",
            "email": "test@example.com",
            "password1": "33Test1234",
            "password2": "33Test1234",
            "track_analytics": False
        }

        form = self.form_class(sample_data)
        form.save()

        self.assertEqual(User.objects.count(), 1)

    def test_registration_post_request_with_valid_data(self):
        sample_data = {
            "username": "TestAccount",
            "email": "test@example.com",
            "password1": "33Test1234",
            "password2": "33Test1234",
            "track_analytics": False
        }
        response = self.client.post(reverse('registration'), sample_data)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username='TestAccount').exists())

    # Test to assure that the form catches invalid usernames

    def test_user_registration_form_with_invalid_username(self):
        # Invalid user name (contains a space)
        sample_data = {
            "username": "bob smith",  # Invalid username format
            "email": "validemail@example.com",
            "password1": "ValidPass1234",
            "password2": "ValidPass1234",
            "track_analytics": True
        }
        form = self.form_class(sample_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    # Test to assure that the form catches invalid emails
    def test_user_registration_form_with_invalid_email(self):
        sample_data = {
            "username": "ValidUser",
            "email": "invalid-email",  # Invalid email format
            "password1": "ValidPass1234",
            "password2": "ValidPass1234",
            "track_analytics": True
        }
        form = self.form_class(sample_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    # Test to assure that the form catches invalid passwords
    # e.g. ['This password is too short. It must contain at least 8 characters.', 'This password is too common.', 'This password is entirely numeric.']
    def test_user_registration_form_with_invalid_password(self):
        sample_data = {
            "username": "ValidUser",
            "email": "validemail@example.com",
            "password1": "123",  # Invalid password: too short, entirely numeric
            "password2": "123",
            "track_analytics": True
        }
        form = self.form_class(sample_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    # Test to assure that the form catches mismatched password verification
    def test_user_registration_form_with_mismatched_password_verification(self):
        sample_data = {
            "username": "ValidUser",
            "email": "validemail@example.com",
            "password1": "33Test1234",
            "password2": "33Test12345",  # Mismatched password
            "track_analytics": True
        }
        form = self.form_class(sample_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
