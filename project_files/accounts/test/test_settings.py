from django.test import TestCase
from ..forms import AccountSettingsForm
from ..models import User
from http import HTTPStatus
from django.urls import reverse


class AccountSettingsTest(TestCase):

    def test_form_remove_default_password_field(self):
        form = AccountSettingsForm()
        # Check if the 'password' field is removed from the form
        self.assertNotIn('password', form.fields)

    def test_form_reject_password_mismatch(self):

        data = {
            'username': 'tester',
            'email': 'tester@mail.dcu.ie',
            'password1': '!tester@123',
            'password2': '!tester@12345'
        }

        form = AccountSettingsForm(data=data)

        # Check if the form is rightfully marked as invalid
        self.assertFalse(form.is_valid())

        # Check if the correct field was marked as an error
        self.assertIn('password2', form.errors)

        # Check that the appropriate error message was returned
        self.assertIn("Passwords don't match.", form.errors['password2'])

    def test_form_reject_invalid_password(self):

        data = {
            'username': 'tester',
            'email': 'tester@mail.dcu.ie',
            'password1': '123',
            'password2': '123'
        }

        form = AccountSettingsForm(data=data)

        # Check if the form is rightfully marked as invalid
        self.assertFalse(form.is_valid())

        # Check if the correct field was marked as an error
        self.assertIn('password1', form.errors)

        # Check if the appropriate error message were returned
        returned_errors = form.errors['password1']

        error_messages = ["This password is too short. It must contain at least 8 characters.",
                          "This password is too common.",
                          "This password is entirely numeric."]

        for error in error_messages:
            self.assertIn(error, returned_errors)

    def test_form_change_username(self):

        original_data = {
            'username': 'original_name',
            'email': 'original@mail.com',
            'password': '@password123!',
            'track_history': 'true'
        }

        # Create a new user with the original data
        user = User.objects.create_user(**original_data)

        # Verify that the username of the new user is currently the original_data username
        self.assertEqual(original_data['username'], user.username)

        # Copy the original_data to new_data and change the username
        new_data = original_data
        new_data['username'] = "new_name"

        # Create a form to apply the new_data to the user
        form = AccountSettingsForm(data=new_data, instance=user)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Apply form changes
        form.save()

        # Reload the user from the database to get updated values
        user.refresh_from_db()

        # Assert that the username has been changed to the new_data username
        self.assertEqual(new_data['username'], user.username)

    def test_form_change_email(self):

        original_data = {
            'username': 'original_name',
            'email': 'original@mail.com',
            'password': '@password123!',
            'track_history': 'true'
        }

        # Create a new user with the original data
        user = User.objects.create_user(**original_data)

        # Verify that the email of the new user is currently the original_data email
        self.assertEqual(original_data['email'], user.email)

        # Copy the original_data to new_data and change the email
        new_data = original_data
        new_data['email'] = "new@mail.com"

        # Create a form to apply the new_data to the user
        form = AccountSettingsForm(data=new_data, instance=user)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Apply form changes
        form.save()

        # Reload the user from the database to get updated values
        user.refresh_from_db()

        # Assert that the email has been changed to the new_data email
        self.assertEqual(new_data['email'], user.email)

    def test_form_change_password(self):

        original_data = {
            'username': 'original_name',
            'email': 'original@mail.com',
            'password': '@password123!',
            'track_history': 'true'
        }

        # Create a new user with the original data
        user = User.objects.create_user(**original_data)

        # Verify that the password of the new user is currently the original_data password
        self.assertTrue(user.check_password(original_data['password']))

        # Copy the original_data to new_data and change the password
        new_data = original_data
        new_data['password1'] = "@newpassword123!"
        new_data['password2'] = "@newpassword123!"

        # Create a form to apply the new_data to the user
        form = AccountSettingsForm(data=new_data, instance=user)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Apply form changes
        form.save()

        # Reload the user from the database to get updated values
        user.refresh_from_db()

        # Assert that the password has been changed to the new_data password
        self.assertTrue(user.check_password(new_data['password1']))
